from typing import List

from sqlalchemy.orm import Session, joinedload

from flask_app.base.repositories import BaseRepository

from .dtos import InventoryItemDTO
from .models import InventoryItem


class InventoryItemRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(InventoryItem, InventoryItemDTO, db_session)

    def _to_dto(self, instance: InventoryItem) -> InventoryItemDTO:
        # Get the associated StoreItem if it's loaded
        store_item = instance.item if hasattr(instance, "item") else None

        return InventoryItemDTO(
            id=instance.id,
            user_id=instance.user_id,
            store_item_id=instance.store_item_id,
            quantity=instance.quantity,
            name=store_item.name if store_item else "",
            image_path=store_item.image_path if store_item else "",
        )

    def _from_dto(self, dto: InventoryItemDTO) -> InventoryItem:
        return InventoryItem(
            id=dto.id,
            user_id=dto.user_id,
            store_item_id=dto.store_item_id,
            quantity=dto.quantity,
        )

    def get_inventory_by_user_id(self, user_id: int) -> List[InventoryItemDTO]:
        # Use joinedload to eager load the StoreItem relationship
        instances = (
            self.db_session.query(self.model)
            .options(joinedload(InventoryItem.item))
            .filter_by(user_id=user_id)
            .all()
        )
        return [self._to_dto(instance) for instance in instances]
