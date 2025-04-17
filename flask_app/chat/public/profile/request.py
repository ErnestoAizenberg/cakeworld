from flask import g, session

from flask_app.forum.category.models import Category
from flask_app.website.editing.models import Server


def setup_request_hooks(app, user_service, profile_service):
    @app.before_request
    def before_request():
        g.categories = Category.query.all()
        user_id = session.get("user_id")

        current_user = user_service.get_user(1) if user_id else None

        try:
            server = Server.get_server()
            g.server_info = server
            print(g.server_info)
        except Exception as ex:
            g.server_info = None
            print(f"Failed to get server info: {ex}")

    @app.after_request
    def after_request(response):
        return response

    @app.context_processor
    def inject_user_and_server():
        user_id = session.get("user_id")
        user = user_service.get_user(user_id) if user_id else None
        server = Server.get_server()
        return dict(user=user, server=server)
