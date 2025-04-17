from datetime import datetime, timedelta

from flask import (Blueprint, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.exceptions import BadRequest, Forbidden


def configure_chat_routes(app, socketio, chat_form, chat_controller, chat_service):

    chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

    @chat_bp.route("/")
    def chat_list():
        chat_list = chat_controller.get_all_chats()
        return render_template(
            "/chat/chat_list.html",
            chat_list=chat_list,
        )

    @chat_bp.route("/create", methods=["GET", "POST"])
    def create_chat():
        """Handle chat creation with form validation."""
        if "user_id" not in session:
            flash("Для создания чата необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        form = chat_form()
        user_id = session["user_id"]

        if form.validate_on_submit():
            result = chat_controller.create_chat(
                {
                    "title": form.title.data,
                    "url_name": form.url_name.data,
                    "is_private": form.is_private.data,
                    "description": form.description.data,
                    "creator_id": user_id,
                }
            )

            if result["status"] == "success":
                flash(result["message"], "success")
                return redirect(
                    url_for("chat.chat_info", url_name=result["chat"]["url_name"])
                )

            flash(result["message"], "error")

        chats = chat_service.get_all_chats()
        return render_template(
            "chat/create_chat.html",
            chats=chats,
            user={"id": user_id},  # Minimal user data
            form=form,
        )

    @chat_bp.route("/<string:url_name>/join", methods=["POST"])
    def join_chat(url_name):
        """Handle joining public chat."""
        if "user_id" not in session:
            flash("Для входа в чат необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        result = chat_controller.join_to_chat(
            user_id=session["user_id"], url_name=url_name
        )

        flash(result["message"], result["status"])
        return redirect(url_for("chat.chat_info", url_name=url_name))

    @chat_bp.route("/<string:url_name>/request", methods=["POST"])
    def request_join_chat(url_name):
        """Handle join requests for private chats."""
        if "user_id" not in session:
            return (
                jsonify({"status": "error", "message": "Authentication required"}),
                401,
            )

        result = chat_controller.send_join_request(
            user_id=session["user_id"], url_name=url_name
        )

        return jsonify(result), 200 if result["status"] == "success" else 400

    @chat_bp.route("/requests/handle", methods=["POST"])
    def handle_join_request():
        """Handle moderation of join requests."""
        if "user_id" not in session:
            flash("Необходимы права модератора", "error")
            return redirect(url_for("auth.login"))

        try:
            message_id = request.form["message_id"]
            action = request.form["action"]
        except KeyError:
            raise BadRequest("Missing required fields")

        result = chat_controller.handle_join_request(
            message_id=message_id, action=action, moderator_id=session["user_id"]
        )

        if result["status"] != "success":
            flash(result["message"], "error")
            return redirect(url_for("main.index"))

        # Get chat URL from controller response if available
        if "chat_url" in result.get("data", {}):
            return redirect(
                url_for("chat.chat_info", url_name=result["data"]["chat_url"])
            )

        flash(result["message"], "success")
        return redirect(url_for("main.index"))

    @chat_bp.route("/<string:url_name>")
    def chat_info(url_name):
        """Display chat information and membership status."""
        if "user_id" not in session:
            flash("Для просмотра чата необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        result = chat_controller.get_chat_info(
            url_name=url_name, user_id=session["user_id"]
        )

        if result["status"] != "success":
            flash(result["message"], "error")
            return redirect(url_for("chat.create_chat"))

        return render_template(
            "chat/chat_info.html",
            chat=result["data"]["chat"],
            is_member=result["data"]["is_member"],
            user={"id": session["user_id"]},  # Minimal user data
        )

    @chat_bp.route("/list")
    def list_chats():
        """List all chats the user is member of."""
        if "user_id" not in session:
            flash("Для просмотра чатов необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        result = chat_controller.list_user_chats(session["user_id"])

        return render_template(
            "chat/chat_list.html",
            chats=result["data"]["chats"],
            user={"id": session["user_id"]},  # Minimal user data
        )

    @chat_bp.route("/<string:url_name>/mute", methods=["POST"])
    def mute_user(url_name):
        """Mute a user in chat (moderator only)."""
        if "user_id" not in session:
            return (
                jsonify({"status": "error", "message": "Authentication required"}),
                401,
            )

        try:
            user_id = int(request.form["user_id"])
            duration = int(request.form["duration"])  # in minutes
            mute_until = datetime.utcnow() + timedelta(minutes=duration)
        except (KeyError, ValueError):
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        result = chat_controller.mute_user_in_chat(
            url_name=url_name,
            user_id=user_id,
            moderator_id=session["user_id"],
            until=mute_until,
        )

        return jsonify(result), 200 if result["status"] == "success" else 403

    # Register blueprint
    app.register_blueprint(chat_bp)

    # Socket.IO handlers would be configured here
    # configure_chat_socketio(socketio, chat_controller)
