from functools import lru_cache
from typing import Any, Dict, List

from flask_app.forum.post.dtos import PostDTO

from .dtos import TopicDTO
from .services import TopicService


class TopicController:
    def __init__(self, topic_service: TopicService):
        self.service = topic_service

    @lru_cache(maxsize=128)
    def get_topic(self, topic_id: int) -> TopicDTO:
        """Получает данные темы по ID"""
        return self.service.get_topic(topic_id)

    @lru_cache(maxsize=128)
    def get_topic_by_url_name(self, url_name: str) -> TopicDTO:
        """Получает данные темы по URL-имени"""
        return self.service.get_topic_by_url_name(url_name)

    @lru_cache(maxsize=128)
    def get_topics_by_category(self, category_id: int) -> List[TopicDTO]:
        """Получает список тем в категории"""
        return self.service.get_topics_by_category(category_id)

    def create_topic(self, form_data: Dict[str, Any], user_id: int) -> TopicDTO:
        """Создает новую тему"""
        topic_dto = TopicDTO(
            title=form_data["title"],
            url_name=form_data["url_name"],
            category_id=form_data["category"],
            created_by=user_id,
            description=form_data.get("description", ""),
        )
        return self.service.create_topic(topic_dto)

    def update_topic(self, topic_id: int, form_data: Dict[str, Any]) -> TopicDTO:
        """Обновляет существующую тему"""
        topic_dto = TopicDTO(
            id=topic_id,
            title=form_data["title"],
            url_name=form_data["url_name"],
            category_id=form_data["category_id"],
            description=form_data.get("description", ""),
        )
        return self.service.update_topic(topic_dto)

    def delete_topic(self, topic_id: int) -> None:
        """Удаляет тему"""
        self.service.delete_topic(topic_id)

    @lru_cache(maxsize=128)
    def get_posts_for_topic(self, topic_id: int) -> List[PostDTO]:
        """Получает посты для темы"""
        return self.service.get_posts_for_topic(topic_id)
