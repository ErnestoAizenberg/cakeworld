import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from flask import (
    Blueprint,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import BadRequest, Forbidden

# Set up logging
logger = logging.getLogger(__name__)


def configure_chat_routes(
    app, socketio, chat_form, chat_controller, chat_service
) -> None:
    """
    Configure all chat-related routes for the Flask application.

    Args:
        app: Flask application instance
        socketio: Socket.IO instance
        chat_form: Chat form class
        chat_controller: Chat controller instance
        chat_service: Chat service instance
    """
    chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

    @chat_bp.route("/")
    def chat_list() -> str:
        """Display a list of all available chats."""
        try:
            chat_list = chat_controller.get_all_chats()
            return render_template(
                "/chat/chat_list.html",
                chat_list=chat_list,
            )
        except Exception as e:
            logger.error(f"Error fetching chat list: {str(e)}")
            flash("An error occurred while loading chats", "error")
            return redirect(url_for("main.index"))

    @chat_bp.route("/create", methods=["GET", "POST"])
    def create_chat() -> str:
        """
        Handle chat creation with form validation.

        Returns:
            Rendered template or redirect response
        """
        if "user_id" not in session:
            flash("Для создания чата необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        form = chat_form()
        user_id = session["user_id"]

        if form.validate_on_submit():
            try:
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
            except Exception as e:
                logger.error(f"Error creating chat: {str(e)}")
                flash("An error occurred while creating the chat", "error")

        try:
            chats = chat_service.get_all_chats()
            return render_template(
                "chat/create_chat.html", chats=chats, user={"id": user_id}, form=form
            )
        except Exception as e:
            logger.error(f"Error loading create chat page: {str(e)}")
            flash("An error occurred while loading the page", "error")
            return redirect(url_for("main.index"))

    @chat_bp.route("/<string:url_name>/join", methods=["POST"])
    def join_chat(url_name: str):
        """
        Handle joining public chat.

        Args:
            url_name: Unique URL identifier for the chat

        Returns:
            Redirect response
        """
        if "user_id" not in session:
            flash("Для входа в чат необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        try:
            result = chat_controller.join_to_chat(
                user_id=session["user_id"], url_name=url_name
            )
            flash(result["message"], result["status"])
        except Exception as e:
            logger.error(f"Error joining chat {url_name}: {str(e)}")
            flash("An error occurred while joining the chat", "error")

        return redirect(url_for("chat.chat_info", url_name=url_name))

    @chat_bp.route("/<string:url_name>/request", methods=["POST"])
    def request_join_chat(url_name: str) -> tuple:
        """
        Handle join requests for private chats.

        Args:
            url_name: Unique URL identifier for the chat

        Returns:
            JSON response with status
        """
        if "user_id" not in session:
            return (
                jsonify({"status": "error", "message": "Authentication required"}),
                401,
            )

        try:
            result = chat_controller.send_join_request(
                user_id=session["user_id"], url_name=url_name
            )
            return jsonify(result), 200 if result["status"] == "success" else 400
        except Exception as e:
            logger.error(f"Error sending join request to {url_name}: {str(e)}")
            return jsonify({"status": "error", "message": "Internal server error"}), 500

    @chat_bp.route("/requests/handle", methods=["POST"])
    def handle_join_request():
        """
        Handle moderation of join requests.

        Returns:
            Redirect response
        """
        if "user_id" not in session:
            flash("Необходимы права модератора", "error")
            return redirect(url_for("auth.login"))

        try:
            message_id = request.form["message_id"]
            action = request.form["action"]
        except KeyError as e:
            logger.warning(f"Missing form field: {str(e)}")
            raise BadRequest("Missing required fields")

        try:
            result = chat_controller.handle_join_request(
                message_id=message_id, action=action, moderator_id=session["user_id"]
            )

            if result["status"] != "success":
                flash(result["message"], "error")
                return redirect(url_for("main.index"))

            if "chat_url" in result.get("data", {}):
                return redirect(
                    url_for("chat.chat_info", url_name=result["data"]["chat_url"])
                )

            flash(result["message"], "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            logger.error(f"Error handling join request: {str(e)}")
            flash("An error occurred while processing the request", "error")
            return redirect(url_for("main.index"))

    @chat_bp.route("/<string:url_name>/info")
    def chat_info(url_name: str):
        """
        Display chat information and membership status.

        Args:
            url_name: Unique URL identifier for the chat

        Returns:
            Rendered template or redirect response
        """
        if "user_id" not in session:
            flash("Для просмотра чата необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        try:
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
                user={"id": session["user_id"]},
            )
        except Exception as e:
            logger.error(f"Error loading chat info for {url_name}: {str(e)}")
            flash("An error occurred while loading chat information", "error")
            return redirect(url_for("main.index"))

    @chat_bp.route("/list")
    def list_chats() -> str:
        """List all chats the user is member of."""
        if "user_id" not in session:
            flash("Для просмотра чатов необходимо авторизоваться", "error")
            return redirect(url_for("auth.login"))

        try:
            result = chat_controller.list_user_chats(session["user_id"])
            return render_template(
                "chat/chat_list.html",
                chats=result["data"]["chats"],
                user={"id": session["user_id"]},
            )
        except Exception as e:
            logger.error(f"Error listing user chats: {str(e)}")
            flash("An error occurred while loading your chats", "error")
            return redirect(url_for("main.index"))

    @chat_bp.route("/<string:url_name>/mute", methods=["POST"])
    def mute_user(url_name: str) -> tuple:
        """
        Mute a user in chat (moderator only).

        Args:
            url_name: Unique URL identifier for the chat

        Returns:
            JSON response with status
        """
        if "user_id" not in session:
            return (
                jsonify({"status": "error", "message": "Authentication required"}),
                401,
            )

        try:
            user_id = int(request.form["user_id"])
            duration = int(request.form["duration"])  # in minutes
            mute_until = datetime.utcnow() + timedelta(minutes=duration)
        except (KeyError, ValueError) as e:
            logger.warning(f"Invalid mute parameters: {str(e)}")
            return jsonify({"status": "error", "message": "Invalid parameters"}), 400

        try:
            result = chat_controller.mute_user_in_chat(
                url_name=url_name,
                user_id=user_id,
                moderator_id=session["user_id"],
                until=mute_until,
            )
            return jsonify(result), 200 if result["status"] == "success" else 403
        except Exception as e:
            logger.error(f"Error muting user in chat {url_name}: {str(e)}")
            return jsonify({"status": "error", "message": "Internal server error"}), 500

    # Register blueprint
    app.register_blueprint(chat_bp)

    # Note: Socket.IO handlers would be configured separately
    # configure_chat_socketio(socketio, chat_controller)
