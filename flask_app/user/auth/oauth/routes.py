from flask import Blueprint, flash, redirect, request, session, url_for

oauth_bp = Blueprint("oauth", __name__)


def configure_oauth_routes(app, oauth_service):

    @oauth_bp.route("/authorize/<provider>")
    def oauth2_authorize(provider):
        print("[DEBUG] HERE WE GO")
        return oauth_service.authorize(provider)

    @oauth_bp.route("/callback/<provider>")
    def oauth2_callback(provider):
        print("[DEBUG] HERE WE GO2")
        return oauth_service.callback(provider, request.args)

    app.register_blueprint(oauth_bp)
