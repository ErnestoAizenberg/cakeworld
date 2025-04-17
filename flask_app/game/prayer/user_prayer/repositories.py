from datetime import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import UserPrayDTO
from .models import UserPray


class UserPrayRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(UserPray, UserPrayDTO, db_session)

    def _to_dto(self, instance: UserPray) -> UserPrayDTO:
        return UserPrayDTO(
            id=instance.id,
            user_id=instance.user_id,
            banner_id=instance.banner_id,
            created_at=instance.created_at,
        )

    def _from_dto(self, dto: UserPrayDTO) -> UserPray:
        return UserPray(
            id=dto.id,
            user_id=dto.user_id,
            banner_id=dto.banner_id,
            created_at=dto.created_at,
        )

    def get_user_pray_by_user_id(self, user_id: int) -> Optional[UserPrayDTO]:
        instance = self.db_session.query(self.model).filter_by(user_id=user_id).first()
        if instance:
            return self._to_dto(instance)
        return None

    def count_today_prayers(self, user_id: int) -> int:
        # Получаем текущую дату
        now = datetime.utcnow()

        # Начало и конец текущего дня
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, 999999)

        # Выполняем запрос с подсчетом количества молитв
        return (
            self.db_session.query(func.count(UserPray.id))
            .filter(
                UserPray.user_id == user_id,
                UserPray.created_at >= start_of_day,
                UserPray.created_at <= end_of_day,
            )
            .scalar()
        )
