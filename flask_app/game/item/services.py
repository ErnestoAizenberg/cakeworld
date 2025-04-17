from typing import List, Optional

from .dtos import StoreItemDTO


class StoreItemService:
    def __init__(self, repository):
        self.repository = repository

    def create_item(self, item_data: dict) -> StoreItemDTO:
        item_dto = StoreItemDTO(**item_data)
        return self.repository.save(item_dto)

    def get_item(self, item_id: int) -> Optional[StoreItemDTO]:
        return self.repository.get(item_id)

    def get_all_items(self) -> List[StoreItemDTO]:
        return self.repository.get_all()

    def update_item(self, item_id: int, item_data: dict) -> Optional[StoreItemDTO]:
        item_data["id"] = item_id
        item_dto = StoreItemDTO(**item_data)
        return self.repository.update(item_dto)

    def delete_item(self, item_id: int) -> bool:
        return self.repository.delete(item_id)
