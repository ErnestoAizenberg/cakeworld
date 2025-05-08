from flask import jsonify, render_template


def configure_site_statistics(app, site_statistic_controller):
    @app.route("/admin/statistics", methods=["GET"])
    def get_all_statistics():
        return jsonify(site_statistic_controller.compile_statistics())

    @app.route("/admin/users/registration_trends", methods=["GET"])
    def get_registration_trends():
        trends = site_statistic_controller.fetch_registration_trends()
        return jsonify(trends)

    @app.route("/admin/messages/sent_trends", methods=["GET"])
    def get_message_sent_trends():
        trends = site_statistic_controller.fetch_message_sent_trends()
        return jsonify(trends)

    @app.route("/admin/posts/created_trends", methods=["GET"])
    def get_post_created_trends():
        trends = site_statistic_controller.fetch_post_created_trends()
        return jsonify(trends)

    @app.route("/admin/chats/user_counts", methods=["GET"])
    def get_chat_user_counts():
        chat_data = site_statistic_controller.fetch_chat_user_counts()
        return jsonify(chat_data)

    @app.route("/admin/messages/unique_user_trends", methods=["GET"])
    def get_unique_user_trends():
        trends = site_statistic_controller.fetch_unique_user_trends()
        return jsonify(trends)

    @app.route("/admin_dashboard")
    def admin_dashboard():
        admin_data = {"chart_data": {"width": 800, "height": 400, "color": "#8B4513"}}
        return render_template(
            "admin_dash.html",
            admin_data=admin_data,
        )

    @app.route("/admin/site_statistics")
    def admin_dash():
        return render_template("website_statistics/plots.html")
