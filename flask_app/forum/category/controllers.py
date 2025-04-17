from typing import List, Optional, Tuple

from .dtos import CategoryDTO


class CategoryController:
    def __init__(self, category_service: "CategoryService", CategoryForm: "FlaskForm"):
        self.category_service = category_service

    def create_category(
        self, name: str, color: str, description: str
    ) -> Tuple[bool, str, Optional[CategoryDTO]]:
        return self.category_service.create_category(name, color, description)

    def get_category_by_name(self, name: str) -> Optional[CategoryDTO]:
        return self.category_service.get_category_by_name(name)

    def get_category_topics(self, category_id) -> List["TopicDTO"]:
        topics_dto = self.category_service.get_category_topics(category_id)
        return topics_dto
