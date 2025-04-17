# flask_app/services/category_service.py
from typing import List, Optional

from ..repositories.category_repository import CategoryRepository
from .dtos.category_dto import CategoryDTO


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get_all(self):
        return self.category_repository.get_all() or []

    def create_category(self, name: str, color: str, description: str) -> CategoryDTO:
        category = self.category_repository.model(
            name=name,
            color=color,
            description=description,
        )
        return self.category_repository.save(category)

    def get_category_by_name(self, name: str) -> Optional[CategoryDto]:
        return self.category_repository.get_all(name=name)[0]
