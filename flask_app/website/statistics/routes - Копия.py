from flask import jsonify, render_template
from sqlalchemy.exc import SQLAlchemyError


def configure_site_statistics(app, site_statistic_controller):
    @app.route("/admin/statistics", methods=["GET"])
    def get_all_statistics():
        try:
            registration_trends = site_statistic_controller.fetch_registration_trends()
            message_sent_trends = site_statistic_controller.fetch_message_sent_trends()
            post_created_trends = site_statistic_controller.fetch_post_created_trends()

            latest_data = {
                "latest_user_registration": site_statistic_controller.get_latest_value(
                    registration_trends
                ),
                "latest_message_sent": site_statistic_controller.get_latest_value(
                    message_sent_trends
                ),
                "latest_post_created": site_statistic_controller.get_latest_value(
                    post_created_trends
                ),
            }

            return jsonify(
                {
                    "user_registration_trends": [
                        {"month": month, "count": count}
                        for month, count in registration_trends
                    ],
                    "message_sent_trends": [
                        {"day": day, "count": count}
                        for day, count in message_sent_trends
                    ],
                    "post_created_trends": [
                        {"week": week, "count": count}
                        for week, count in post_created_trends
                    ],
                    "latest_data": latest_data,
                }
            )

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    @app.route("/admin/users/registration_trends", methods=["GET"])
    def get_registration_trends():
        trends = fetch_registration_trends()
        return jsonify([{"month": month, "count": count} for month, count in trends])

    @app.route("/admin/messages/sent_trends", methods=["GET"])
    def get_message_sent_trends():
        trends = fetch_message_sent_trends()
        return jsonify([{"day": day, "count": count} for day, count in trends])

    @app.route("/admin/posts/created_trends", methods=["GET"])
    def get_post_created_trends():
        trends = fetch_post_created_trends()
        return jsonify([{"week": week, "count": count} for week, count in trends])

    @app.route("/admin/chats/user_counts", methods=["GET"])
    def get_chat_user_counts():
        chat_data = fetch_chat_user_counts()
        return jsonify(chat_data)

    @app.route("/admin/messages/unique_user_trends", methods=["GET"])
    def get_unique_user_trends():
        trends = fetch_unique_user_trends()
        return jsonify(
            [{"day": day, "unique_users": unique_users} for day, unique_users in trends]
        )

    @app.route("/admin_dashboard")
    def admin_dashboard():
        admin_data = {"chart_data": {"width": 800, "height": 400, "color": "#8B4513"}}
        return render_template(
            "admin_dash.html",
            admin_data=admin_data,
        )

    @app.route("/admin/site_statistics")
    def admin_dash():
        # make complex check
        return render_template("website_statistics/plots.html")
