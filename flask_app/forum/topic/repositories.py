from typing import List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository
from flask_app.forum.post.dtos import PostDTO

from .dtos import TopicDTO
from .models import Topic


class TopicRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Topic, TopicDTO, db_session)

    def _to_dto(self, instance: Topic) -> TopicDTO:
        """Преобразует модель Topic в TopicDTO"""
        return TopicDTO(
            id=instance.id,
            title=instance.title,
            url_name=instance.url_name,
            description=instance.description,
            category_id=instance.category_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
            created_by=instance.created_by,
        )

    def _from_dto(self, dto: TopicDTO) -> Topic:
        """Преобразует TopicDTO в модель Topic"""
        return Topic(
            # id=dto.id,
            title=dto.title,
            url_name=dto.url_name,
            description=dto.description,
            category_id=dto.category_id,
            created_by=dto.created_by,
        )

    def get_by_url_name(self, url_name: str) -> Optional[TopicDTO]:
        """Получает тему по URL-имени"""
        topic = self.db_session.query(self.model).filter_by(url_name=url_name).first()
        return self._to_dto(topic) if topic else None

    def get_all_by_category(self, category_id: int) -> List[TopicDTO]:
        """Получает все темы в категории"""
        topics = (
            self.db_session.query(self.model).filter_by(category_id=category_id).all()
        )
        return [self._to_dto(topic) for topic in topics]

    def get_posts_for_topic(self, topic_id: int) -> List[PostDTO]:
        """Получает все посты в теме"""
        topic = self.db_session.query(self.model).get(topic_id)
        if not topic:
            return []

        return [
            PostDTO(
                id=post.id,
                title=post.title,
                content=post.content,
                topic_id=post.topic_id,
                user_id=post.user_id,
                created=post.created,
                images=post.images,
                views=post.views,
                post_id=post.post_id,
            )
            for post in topic.posts
        ]
