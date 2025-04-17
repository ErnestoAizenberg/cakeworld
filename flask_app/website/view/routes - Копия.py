from flask import render_template, session


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
