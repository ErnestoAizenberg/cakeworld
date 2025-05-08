from flask import jsonify, request, session

from .services import NotificationService


class NotificationController:
    def __init__(self,
        notification_service: NotificationService
     ):
        self.service = notification_service

    def mark_notification_as_read(self, notification_id):
        #TO CHECK: notification_id is int or str?
        notification_dto = self.service.mark_notification_as_read(notification_id)
        if notification_dto is None:
            return jsonify({"error": "Notification not found"}), 404

        if notification_dto.user_id != session.get("user_id"):
            return (
                jsonify(
                    {"error": "You do not have permission to access this notification"}
                ),
                403,
            )

        return jsonify({"message": "Notification marked as read"}), 200

    def get_notifications_count(self, user_id):
        count = self.service.get_unread_notifications_count(user_id)
        return jsonify({"count": count})

    def get_notifications(self, user_id):
        notifications = self.service.get_notifications(user_id)
        return jsonify([n for n in notifications]), 200

    def get_notification(self, notification_id):
        notification_dto = self.service.get_notification(notification_id)
        if notification_dto is None:
            return jsonify({"message": "Notification not found"}), 404
        return jsonify(notification_dto.dict()), 200

    def add_notification(self, data):
        data = request.json
        notification_dto = self.service.add_notification(
            user_id=data["user_id"],
            message=data["message"],
            type=data.get("type", "info"),
        )
        return (
            jsonify({"message": "Notification added!", "id": notification_dto.id}),
            201,
        )

    def update_notification(self, notification_id):
        notification_dto = self.service.get_notification(notification_id)
        if notification_dto is None:
            return jsonify({"message": "Notification not found"}), 404

        data = request.json
        notification_dto.is_read = data.get("is_read", notification_dto.is_read)
        updated_dto = self.service.update_notification(notification_dto)
        return jsonify({"message": "Notification updated!"}), 200

    def delete_notification(self, notification_id):
        if self.service.delete_notification(notification_id):
            return jsonify({"message": "Notification deleted!"}), 200
        return jsonify({"message": "Notification not found"}), 404
