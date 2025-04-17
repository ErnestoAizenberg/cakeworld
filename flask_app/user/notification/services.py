from typing import List, Optional

from .dtos import NotificationDTO


class NotificationService:
    def __init__(self, repository: "NotificationRepository"):
        self.repository = repository

    def mark_notification_as_read(
        self, notification_id: int
    ) -> Optional[NotificationDTO]:
        return self.repository.mark_as_read(notification_id)

    def get_unread_notifications_count(self, user_id: int) -> int:
        return self.repository.get_unread_count(user_id)

    def get_notifications(self, user_id: int) -> List[NotificationDTO]:
        return self.repository.get_notifications_by_user(user_id)

    def get_notification(self, notification_id: int) -> Optional[NotificationDTO]:
        return self.repository.get(notification_id)

    def add_notification(
        self, user_id: int, message: str, type: str = "info"
    ) -> NotificationDTO:
        notification_dto = NotificationDTO(
            user_id=user_id,
            message=message,
            type=type,
            is_read=False,
        )
        return self.repository.save(notification_dto)

    def update_notification(self, notification_dto: NotificationDTO) -> NotificationDTO:
        return self.repository.update(notification_dto)

    def delete_notification(self, notification_id: int) -> bool:
        notification_dto = self.repository.get(notification_id)
        if notification_dto:
            return self.repository.delete(notification_dto)
        return False
