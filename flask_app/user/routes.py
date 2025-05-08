# flask_app/routes/user.py
from flask import (
    jsonify,
    render_template,
)


def configure_user_routes(app, controller):
    @app.route("/users")
    def list_users():
        users = controller.list_users()
        print("users: ", users)
        return render_template("/user/list_users.html", users=users)

    @app.route("/api/users", methods=["GET"])
    def get_all_users():
        users = controller.get_all_users()
        return jsonify(users)
