from typing import Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import CurrencyDTO
from .models import Currency


class CurrencyRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Currency, CurrencyDTO, db_session)

    def _to_dto(self, instance: Currency) -> CurrencyDTO:
        return CurrencyDTO(
            id=instance.id,
            user_id=instance.user_id,
            coins=instance.coins,
            stones=instance.stones,
            gems=instance.gems,
        )

    def _from_dto(self, dto: CurrencyDTO) -> Currency:
        return Currency(
            id=dto.id,
            user_id=dto.user_id,
            coins=dto.coins,
            stones=dto.stones,
            gems=dto.gems,
        )

    def get_currency_by_user_id(self, user_id: int) -> Optional[CurrencyDTO]:
        instance = self.db_session.query(self.model).filter_by(user_id=user_id).first()
        if instance:
            return self._to_dto(instance)
        return None
