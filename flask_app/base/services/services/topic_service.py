# flask_app/services/topic_service.py
from typing import List

from ..dto.topic_dto import TopicDTO
from ..repositories.topic_repository import TopicRepository


class TopicService:
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    def get_topics_by_category(self, category_id: int) -> List[TopicDTO]:
        return self.topic_repository.get_all(category_id=category_id)
