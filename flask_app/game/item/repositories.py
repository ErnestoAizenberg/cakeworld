from typing import Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import StoreItemDTO
from .models import StoreItem


class StoreItemRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(StoreItem, StoreItemDTO, db_session)

    def _to_dto(self, instance: StoreItem) -> StoreItemDTO:
        return StoreItemDTO(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            price_coins=instance.price_coins,
            price_gems=instance.price_gems,
            image_path=instance.image_path,
            rarity=instance.rarity,
        )

    def _from_dto(self, dto: StoreItemDTO) -> StoreItem:
        return StoreItem(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            price_coins=dto.price_coins,
            price_gems=dto.price_gems,
            image_path=dto.image_path,
            rarity=dto.rarity,
        )

    def get_store_item_by_id(self, item_id: int) -> Optional[StoreItemDTO]:
        instance = self.db_session.query(self.model).filter_by(id=item_id).first()
        if instance:
            return self._to_dto(instance)
        return None
