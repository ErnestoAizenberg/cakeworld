import json
import logging
from typing import List, Optional

import redis

from flask_app.forum.post.dtos import PostDTO

from .dtos import TopicDTO
from .exceptions import DuplicateUrlNameError, TopicNotFoundError
from .repositories import TopicRepository

# Настройка логирования
logging.basicConfig(
    level=logging.INFO
)  # Уровень логирования (DEBUG, INFO, WARNING, ERROR)
logger = logging.getLogger(__name__)


class TopicService:
    def __init__(
        self, topic_repository: TopicRepository, redis_client: redis.Redis = None
    ):
        self.repository = topic_repository
        self.redis = redis_client
        self.cache_prefix = "topic:"

    def _get_from_cache(self, key: str) -> Optional[TopicDTO]:
        """Получает данные из кэша Redis"""
        if not self.redis:
            return None

        cached_data = self.redis.get(f"{self.cache_prefix}{key}")
        if cached_data:
            logger.info(f"Данные получены из кэша для ключа: {key}")
            return TopicDTO(**json.loads(cached_data))

        logger.warning(f"Данные не найдены в кэше для ключа: {key}")
        return None

    def _set_to_cache(self, key: str, topic: TopicDTO, ttl: int = 3600) -> None:
        """Сохраняет данные в кэш Redis"""
        if self.redis:
            self.redis.setex(
                f"{self.cache_prefix}{key}",
                ttl,
                json.dumps(self._serialize_topic(topic)),
            )
            logger.info(f"Данные сохранены в кэше для ключа: {key}")

    def get_topic(self, topic_id: int) -> TopicDTO:
        """Получает тему по ID с кэшированием"""
        cache_key = f"id:{topic_id}"
        cached_topic = self._get_from_cache(cache_key)
        if cached_topic:
            return cached_topic

        topic = self.repository.get(topic_id)
        if not topic:
            logger.error(f"Тема с ID {topic_id} не найдена")
            raise TopicNotFoundError(f"Тема с ID {topic_id} не найдена")

        self._set_to_cache(cache_key, topic)
        return topic

    def get_topic_by_url_name(self, url_name: str) -> TopicDTO:
        """Получает тему по URL-имени с кэшированием"""
        cache_key = f"url:{url_name}"
        cached_topic = self._get_from_cache(cache_key)
        if cached_topic:
            return cached_topic

        topic = self.repository.get_by_url_name(url_name)
        if not topic:
            logger.error(f"Тема с URL '{url_name}' не найдена")
            raise TopicNotFoundError(f"Тема с URL '{url_name}' не найдена")

        self._set_to_cache(cache_key, topic)
        return topic

    def get_topics_by_category(self, category_id: int) -> List[TopicDTO]:
        """Получает темы по категории"""
        return self.repository.get_all_by_category(category_id)

    def create_topic(self, topic_dto: TopicDTO) -> TopicDTO:
        """Создает новую тему и инвалидирует кэш"""
        if self.repository.get_by_url_name(topic_dto.url_name):
            logger.error(f"URL '{topic_dto.url_name}' уже используется")
            raise DuplicateUrlNameError(f"URL '{topic_dto.url_name}' уже используется")

        topic = self.repository.save(topic_dto)
        # Инвалидация кэша для списка тем категории
        if self.redis:
            self.redis.delete(f"{self.cache_prefix}category:{topic.category_id}")
            logger.info(f"Кэш для категории {topic.category_id} был инвалидацией.")
        return topic

    def update_topic(self, topic_dto: TopicDTO) -> TopicDTO:
        """Обновляет тему и инвалидирует кэш"""
        existing = self.repository.get(topic_dto.id)
        if not existing:
            logger.error(f"Тема с ID {topic_dto.id} не найдена для обновления")
            raise TopicNotFoundError(f"Тема с ID {topic_dto.id} не найдена")

        if topic_dto.url_name != existing.url_name and self.repository.get_by_url_name(
            topic_dto.url_name
        ):
            logger.error(f"URL '{topic_dto.url_name}' уже используется для другой темы")
            raise DuplicateUrlNameError(f"URL '{topic_dto.url_name}' уже используется")

        updated = self.repository.update(topic_dto)
        # Инвалидация кэша
        if self.redis:
            self.redis.delete(
                f"{self.cache_prefix}id:{updated.id}",
                f"{self.cache_prefix}url:{updated.url_name}",
                f"{self.cache_prefix}category:{updated.category_id}",
            )
            logger.info(f"Кэш был инвалидирован для темы ID {updated.id}.")
        return updated

    def delete_topic(self, topic_id: int) -> None:
        """Удаляет тему и инвалидирует кэш"""
        topic = self.repository.get(topic_id)
        if not topic:
            logger.error(f"Тема с ID {topic_id} не найдена для удаления")
            raise TopicNotFoundError(f"Тема с ID {topic_id} не найдена")

        self.repository.delete(topic)
        # Инвалидация кэша
        if self.redis:
            self.redis.delete(
                f"{self.cache_prefix}id:{topic_id}",
                f"{self.cache_prefix}url:{topic.url_name}",
                f"{self.cache_prefix}category:{topic.category_id}",
            )
            logger.info(f"Кэш был инвалидирован для темы ID {topic_id}.")

    def get_posts_for_topic(self, topic_id: int) -> List[PostDTO]:
        """Получает посты для темы"""
        if not self.repository.get(topic_id):
            logger.error(f"Тема с ID {topic_id} не найдена при получении постов.")
            raise TopicNotFoundError(f"Тема с ID {topic_id} не найдена")

        posts = self.repository.get_posts_for_topic(topic_id)
        return [post for post in posts if post] if posts else []

    def _serialize_topic(self, topic: TopicDTO) -> dict:
        """Сериализует TopicDTO для Redis"""
        return {
            "id": topic.id,
            "title": topic.title,
            "url_name": topic.url_name,
            "description": topic.description,
            "category_id": topic.category_id,
            "created_at": topic.created_at.isoformat() if topic.created_at else None,
            "updated_at": topic.updated_at.isoformat() if topic.updated_at else None,
            "created_by": topic.created_by,
        }
