# flask_app/services/forum/category_service.py
from typing import List, Optional

from .dtos import CategoryDTO
from .repositories import CategoryRepository


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        topic_repository: "TopicRepository",
    ):
        self.category_repository = category_repository
        self.topic_repository = topic_repository

    def get_category_topics(self, category_id) -> List["TopicDTO"]:
        """receiving topics with getted id"""
        category_topics_list = (
            self.topic_repository.get_all(category_id=category_id) or []
        )
        # validation ?
        return category_topics_list

    def get_all(self):
        return self.category_repository.get_all() or []

    def create_category(self, name: str, color: str, description: str) -> CategoryDTO:
        category = self.category_repository.model(
            name=name,
            color=color,
            description=description,
        )
        return self.category_repository.save(category)

    def get_category_by_name(self, name: str) -> Optional[CategoryDTO]:
        return self.category_repository.get_all(name=name)[0]
