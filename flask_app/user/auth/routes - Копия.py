# flask_app/user/auth/routes.py
from flask import Blueprint, g, request

auth_bp = Blueprint("auth", __name__)


def init_auth_routes(app, auth_controller):

    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        return auth_controller.register(
            data.get("username"),
            data.get("email"),
            data.get("password"),
            data.get("confirm_password"),
        )

    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        return auth_controller.login(data.get("email"), data.get("password"))

    @auth_bp.route("/verify/<token>", methods=["GET"])
    def verify_email(token):
        return auth_controller.verify_email(token)

    @auth_bp.route("/resend-verification", methods=["POST"])
    def resend_verification():
        data = request.get_json()
        return auth_controller.resend_verification(data.get("email"))

    @auth_bp.route("/request-password-reset", methods=["POST"])
    def request_password_reset():
        data = request.get_json()
        return auth_controller.request_password_reset(data.get("email"))

    @auth_bp.route("/reset-password/<token>", methods=["POST"])
    def reset_password(token):
        data = request.get_json()
        return auth_controller.reset_password(
            token, data.get("new_password"), data.get("confirm_password")
        )

    @auth_bp.route("/logout", methods=["POST"])
    def logout():
        return auth_controller.logout()

    app.register_blueprint(auth_bp, url_prefix="/auth")
