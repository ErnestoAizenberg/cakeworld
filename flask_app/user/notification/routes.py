from flask import render_template


def configure_notification_routes(app, notification_controller):
    @app.route("/notifications")
    def notifications():
        return render_template(
            "notification/notifications.html",
        )

    @app.route("/notifications/<int:notification_id>/mark_as_read", methods=["POST"])
    def mark_notification_as_read(notification_id):
        return notification_controller.mark_notification_as_read(notification_id)

    @app.route("/notifications/<int:user_id>/count", methods=["GET"])
    def get_notifications_count(user_id):
        return notification_controller.get_notifications_count(user_id)

    @app.route("/notifications/<int:user_id>", methods=["GET"])
    def get_notifications(user_id):
        return notification_controller.get_notifications(user_id)

    @app.route("/notifications/<int:notification_id>", methods=["GET"])
    def get_notification(notification_id):
        return notification_controller.get_notification(notification_id)

    @app.route("/notifications", methods=["POST"])
    def add_notification():
        return notification_controller.add_notification()

    @app.route("/notifications/<int:notification_id>", methods=["PUT"])
    def update_notification(notification_id):
        return notification_controller.update_notification(notification_id)

    @app.route("/notifications/<int:notification_id>", methods=["DELETE"])
    def delete_notification(notification_id):
        return notification_controller.delete_notification(notification_id)
