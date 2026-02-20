from flask import Flask, Blueprint, render_template

main_bp = Blueprint("main", __name__)


def configure_pages(app: Flask) -> None:
    @app.route("/")
    @app.route("/index")
    def index_dash():
        return render_template("index.html")

    @app.route("/chats")
    def chats_dashboard():
        return render_template("chats.html")

    @main_bp.route("/b")
    def base():
        return render_template("base.html")

    app.register_blueprint(main_bp)
