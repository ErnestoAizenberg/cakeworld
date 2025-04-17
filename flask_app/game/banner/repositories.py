from typing import List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import BannerDTO
from .models import Banner


class BannerRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Banner, BannerDTO, db_session)

    def _to_dto(self, instance: Banner) -> BannerDTO:
        return BannerDTO(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            icon=instance.icon,
            created_at=instance.created_at,
            logic=instance.logic,
        )

    def _from_dto(self, dto: BannerDTO) -> Banner:
        return Banner(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            icon=dto.icon,
            created_at=dto.created_at,
            logic=dto.logic,
        )

    def get_banner_by_id(self, banner_id: int) -> Optional[BannerDTO]:
        instance = self.db_session.query(self.model).filter_by(id=banner_id).first()
        if instance:
            return self._to_dto(instance)
        return None
