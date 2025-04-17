from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import CategoryDTO
from .models import Category


class CategoryRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Category, CategoryDTO, db_session)

    def _to_dto(self, instance: Category) -> CategoryDTO:
        return CategoryDTO(
            id=instance.id,
            name=instance.name,
            color=instance.color,
            description=instance.description,
            # topics=[self._to_dto(t) for t in instance.topics],
        )
