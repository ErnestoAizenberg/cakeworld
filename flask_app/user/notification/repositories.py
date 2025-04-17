from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import NotificationDTO
from .models import Notification


class NotificationRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Notification, NotificationDTO, db_session)

    def _to_dto(self, instance: Notification) -> NotificationDTO:

        return NotificationDTO(
            id=instance.id,
            user_id=instance.user_id,
            message=instance.message,
            type=instance.type,
            is_read=instance.is_read,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )

    def _from_dto(self, dto: NotificationDTO) -> Notification:
        return Notification(
            user_id=dto.user_id,
            message=dto.message,
            type=dto.type,
            is_read=dto.is_read,
        )

    def get_unread_count(self, user_id: int) -> int:
        return (
            self.db_session.query(self.model)
            .filter_by(user_id=user_id, is_read=False)
            .count()
        )

    def get_notifications_by_user(self, user_id: int) -> List[NotificationDTO]:
        return self.get_all(user_id=user_id)

    def mark_as_read(self, notification_id: int) -> Optional[NotificationDTO]:
        notification = self.db_session.query(self.model).get(notification_id)
        if notification:
            notification.is_read = True
            self.db_session.commit()
            return self._to_dto(notification)
        return None
