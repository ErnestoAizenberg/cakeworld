import uuid
from typing import Dict, List, Optional

from .models import Item, ItemCode, ItemImage
from .repositories import ItemCodeRepository, ItemImageRepository, ItemRepository


class ItemCodeService:
    def __init__(self, item_code_repository: ItemCodeRepository):
        self.item_code_repository = item_code_repository

    def generate_item_codes(self, item_name: str, count: int) -> None:
        """Генерирует новые коды для предметов."""
        for _ in range(count):
            code = f"ITEM-{uuid.uuid4().hex[:8].upper()}"
            item_code = ItemCode(code=code, item_name=item_name)
            self.item_code_repository.save(item_code)

    def get_codes_by_item_name(self, item_name: str) -> List[ItemCode]:
        """Возвращает все коды для указанного предмета."""
        return self.item_code_repository.get_all(item_name=item_name)

    def delete_codes_by_item_name(self, item_name: str) -> None:
        """Удаляет все коды для указанного предмета."""
        codes = self.item_code_repository.get_all_by_item_name(item_name=item_name)
        for code in codes:
            self.item_code_repository.delete(code)
