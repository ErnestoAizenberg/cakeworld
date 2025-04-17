from flask import Blueprint, jsonify, render_template, request, session

main_bp = Blueprint("main", __name__)


def configure_pages(app, user_service):

    @app.route("/b")
    def base():
        return render_template("base.html")

    @app.route("/")
    @app.route("/index")
    def index_dash():
        return render_template("index.html")

    @app.route("/chats")
    def chats_dashboard():
        # get chats
        return render_template("chats.html")

    @main_bp.route("/b")
    def base():
        return render_template("base.html")

    @main_bp.route("/")
    @main_bp.route("/index")
    def index():
        return render_template("index.html")

    @main_bp.route("/chats")
    def chats_dashboard():
        # get chats
        return render_template("chats.html")

    app.register_blueprint(main_bp)
