import logging
from typing import Any, Dict, Optional

from flask import abort, jsonify, redirect, render_template, request, session, url_for
from flask_socketio import emit

# Configure logging
logger = logging.getLogger(__name__)


class DirectChatRoutes:
    """Class to configure and handle direct chat related routes and socket events."""

    def __init__(self, app, socketio, user_service, direct_chat_service):
        """
        Initialize with Flask app, SocketIO, and required services.

        Args:
            app: Flask application instance
            socketio: SocketIO instance
            user_service: User service instance
            direct_chat_service: DirectChat service instance
        """
        self.app = app
        self.socketio = socketio
        self.user_service = user_service
        self.direct_chat_service = direct_chat_service
        self._configure_routes()
        self._configure_socket_events()

    def _configure_routes(self):
        """Configure all direct chat related HTTP routes."""

        @self.app.route("/<string:profile_url>/direct_chat", methods=["GET", "POST"])
        def direct_chat(profile_url: str):
            """Handle direct chat page requests."""
            try:
                viewer_id = session.get("user_id")
                owner_id = self._extract_user_id_from_url(profile_url)

                viewer = self.user_service.get_user(viewer_id)
                owner = self.user_service.get_user(owner_id)
                self._validate_users(viewer, owner)

                if viewer.id == owner.id:
                    return self._handle_self_chat_request(profile_url)

                print("__--__", viewer.id, owner.id)
                chat = self.direct_chat_service.get_or_create_direct_chat(
                    user1_id=owner.id, user2_id=viewer.id
                )
                unread_count = (
                    0  # self.direct_chat_service.get_unread_count(chat.id, viewer.id)
                )

                return render_template(
                    "direct_chat.html",
                    direct_chat=chat,
                    viewer=viewer,
                    owner=owner,
                    user=viewer,
                    unread_count=unread_count,
                )

            except ValueError as e:
                logger.error(f"Validation error in direct_chat: {str(e)}")
                abort(400, description=str(e))
            except Exception as e:
                logger.error(f"Error in direct_chat: {str(e)}")
                abort(500)

        @self.app.route("/load_direct_chat_messages", methods=["GET"])
        def load_direct_chat_messages():
            """Load messages for a direct chat."""
            try:
                user_id = session.get("user_id")
                chat_id = request.args.get("chat_id")
                owner_id = request.args.get("owner_id")
                limit = int(request.args.get("limit", 20))
                offset = int(request.args.get("offset", 0))

                self._validate_chat_request(chat_id, owner_id)

                messages = self.direct_chat_service.get_direct_messages(
                    chat_id=chat_id, user_id=user_id, limit=limit, offset=offset
                )

                return jsonify({"messages": messages}), 200

            except ValueError as e:
                logger.warning(
                    f"Invalid request in load_direct_chat_messages: {str(e)}"
                )
                return jsonify({"error": str(e)}), 400
            except Exception as e:
                logger.error(f"Error in load_direct_chat_messages: {str(e)}")
                return jsonify({"error": "Internal server error"}), 500

        @self.app.route("/view_direct_message/<int:message_id>", methods=["POST"])
        def view_direct_message(message_id: int):
            """Mark a direct message as viewed."""
            try:
                user_id = session.get("user_id")
                if not user_id:
                    return jsonify({"error": "Unauthorized"}), 401

                self.direct_chat_service.mark_direct_message_read(message_id, user_id)
                return jsonify({"status": "success"}), 200

            except Exception as e:
                logger.error(f"Error in view_direct_message: {str(e)}")
                return jsonify({"error": str(e)}), 500

    def _configure_socket_events(self):
        """Configure all direct chat related SocketIO events."""

        @self.socketio.on("send_message")
        def handle_send_message(data: Dict[str, Any]):
            """Handle sending a new message via websocket."""
            try:
                self._validate_message_data(data)

                message = self.direct_chat_service.send_direct_message(
                    chat_id=data["chat_id"],
                    author_id=data["user_id"],
                    text=data["text"],
                )

                emit(
                    "new_message",
                    {
                        "id": message["id"],
                        "author": message["user_id"],
                        "text": message["text"],
                        "created": message["created"],
                    },
                    room=data["chat_id"],
                )

            except ValueError as e:
                logger.warning(f"Invalid message data: {str(e)}")
                emit("error", {"message": str(e)})
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                emit("error", {"message": "Internal server error"})

        @self.socketio.on("mark_as_read")
        def handle_mark_as_read(data: Dict[str, Any]):
            """Handle marking a message as read via websocket."""
            try:
                self._validate_read_request(data)

                self.direct_chat_service.mark_direct_message_read(
                    message_id=data["message_id"], reader_id=data["user_id"]
                )

                emit(
                    "message_read",
                    {"message_id": data["message_id"], "user_id": data["user_id"]},
                    room=data["chat_id"],
                )

            except ValueError as e:
                logger.warning(f"Invalid read request: {str(e)}")
            except Exception as e:
                logger.error(f"Error marking message as read: {str(e)}")

    # Helper methods
    def _extract_user_id_from_url(self, profile_url: str) -> int:
        """Extract user ID from profile URL."""
        try:
            return int(profile_url.split(".")[-1])
        except (IndexError, ValueError):
            raise ValueError("Invalid profile URL format")

    def _validate_users(self, viewer: Optional[Any], owner: Optional[Any]):
        """Validate that both users exist."""
        if not owner:
            raise ValueError("User not found")
        if not viewer:
            raise ValueError("Unauthorized access")

    def _validate_chat_request(self, chat_id: Optional[str], owner_id: Optional[str]):
        """Validate chat message loading request."""
        if not chat_id:
            raise ValueError("Chat ID is required")
        if not owner_id:
            raise ValueError("Owner ID is required")

    def _validate_message_data(self, data: Dict[str, Any]):
        """Validate message data from websocket."""
        required_fields = ["user_id", "chat_id", "text", "owner_id"]
        if not all(field in data for field in required_fields):
            raise ValueError("Missing required fields in message data")

    def _validate_read_request(self, data: Dict[str, Any]):
        """Validate mark as read request."""
        if not all(key in data for key in ["user_id", "message_id", "chat_id"]):
            raise ValueError("Invalid read message data")

    def _handle_self_chat_request(self, profile_url: str):
        """Handle case when user tries to chat with themselves."""
        if request.method == "POST":
            return jsonify({"error": "You can't send messages to yourself"}), 400

        unread_messages_amount = 0  # Replace with actual unread count logic
        return redirect(url_for("notifications", unread_count=unread_messages_amount))
