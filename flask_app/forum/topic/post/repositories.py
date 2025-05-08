from typing import List

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import PostDTO
from .models import Post


class PostRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Post, PostDTO, db_session)

    def _to_dto(self, instance: Post) -> PostDTO:
        """Преобразует модель Post в PostDTO."""
        return PostDTO(
            id=instance.id,
            title=instance.title,
            content=instance.content,
            user_id=instance.user_id,
            topic_id=instance.topic_id,
            post_id=instance.post_id,
            created=instance.created,
            images=instance.images,
            views=instance.views,
        )

    def _from_dto(self, dto: PostDTO) -> Post:
        """Преобразует PostDTO в модель Post."""
        return Post(
            id=dto.id,
            title=dto.title,
            content=dto.content,
            user_id=dto.user_id,
            topic_id=dto.topic_id,
            post_id=dto.post_id,
            created=dto.created,
            images=dto.images,
            views=dto.views,
        )

    def get_all_posts(self):
        return (
            self.db_session.query(self.model)
            .filter_by(topic_id=topic.id, post_id=None)
            .all()
        )

    def get_posts_by_user(self, user_id: int) -> List[PostDTO]:
        """Возвращает все посты пользователя."""
        return self.get_all(user_id=user_id, post_id=None)

    def count_user_posts(self, user_id: int) -> int:
        """Возвращает количество постов пользователя."""
        return len(self.get_all(user_id=user_id, post_id=None))
