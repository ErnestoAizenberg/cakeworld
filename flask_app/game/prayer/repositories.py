from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import PrayerResultDTO
from .models import PrayerResult


class PrayerResultRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(PrayerResult, PrayerResultDTO, db_session)

    def _to_dto(self, instance: PrayerResult) -> PrayerResultDTO:
        return PrayerResultDTO(
            id=instance.id,
            user_id=instance.user_id,
            item_id=instance.item_id,
            banner_id=instance.banner_id,
            created_at=instance.created_at,
        )

    def _from_dto(self, dto: PrayerResultDTO) -> PrayerResult:
        return PrayerResult(
            id=dto.id,
            user_id=dto.user_id,
            item_id=dto.item_id,
            banner_id=dto.banner_id,
            created_at=dto.created_at,
        )

    def count_today_prayers(self, user_id: int) -> int:
        # Получаем текущую дату
        now = datetime.utcnow()

        # Начало и конец текущего дня
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59, 999999)

        # Выполняем запрос с подсчетом количества молитв
        return (
            self.db_session.query(func.count(PrayerResult.id))
            .filter(
                PrayerResult.user_id == user_id,
                PrayerResult.created_at >= start_of_day,
                PrayerResult.created_at <= end_of_day,
            )
            .scalar()
        )
