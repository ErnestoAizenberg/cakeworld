from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import BannedUserDTO
from .models import BannedUser


class BannedUserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(BannedUser, BannedUserDTO, db_session)

    def _to_dto(self, instance: BannedUser) -> BannedUserDTO:
        """Преобразует модель BannedUser в BannedUserDTO."""
        return BannedUserDTO(
            id=instance.id,
            user_id=instance.user_id,
            created=instance.created,
            ban_until=instance.ban_until,
            reason=instance.reason,
            ban_type=instance.ban_type,
        )

    def _from_dto(self, dto: BannedUserDTO) -> BannedUser:
        """Преобразует BannedUserDTO в модель BannedUser."""
        return BannedUser(
            id=dto.id,
            user_id=dto.user_id,
            created=dto.created,
            ban_until=dto.ban_until,
            reason=dto.reason,
            ban_type=dto.ban_type,
        )

    def get_active_bans_by_user_id(self, user_id: str) -> List[BannedUserDTO]:
        """Получает все активные баны для пользователя."""
        bans = (
            self.db_session.query(self.model)
            .filter(
                self.model.user_id == user_id, self.model.ban_until > datetime.utcnow()
            )
            .all()
        )
        return [self._to_dto(ban) for ban in bans]
