import logging

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_socketio import emit, join_room, leave_room


def configure_real_time_chating(
    app,
    socketio,
    csrf,
    chat_service,
    message_service,
    chat_avatar_service=None,  # TO REMOVE
):
    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    @app.route("/chat/<string:url_name>", methods=["GET"])
    @csrf.exempt
    def chat_deb(url_name):
        chat = chat_service.get_chat_by_url(url_name)

        user = g.current_user
        user_chats = chat_service.get_user_chats(user.id)
        unread_count = message_service.get_unread_count(chat.id, user.id)
        user_in_chat = chat_service.is_user_in_chat(user.id, chat.id)

        chat_users = chat_service.get_chat_users(chat.id)
        chat_avatar_path = chat_avatar_service.get_avatar_path(chat)

        return render_template(
            "chat/chat.html",
            chat=chat,
            user_inchat=user_in_chat,
            users=chat_users,
            user_chats=user_chats,
            unread_count=unread_count,
            chat_avatar_path=chat_avatar_path,
        )

    @app.route("/chatDE/<string:url_name>", methods=["GET"])
    @csrf.exempt
    def chat(url_name):
        logger.debug("opening chat... ")
        chat = chat_service.get_chat_by_url(url_name)
        if not chat:
            abort(404)

        user = g.current_user
        user_chats = chat_service.get_user_chats(user.id)
        unread_count = message_service.get_unread_count(chat.id, user.id)
        user_in_chat = chat_service.is_user_in_chat(user.id, chat.id)
        chat_users = chat_service.get_chat_users(chat.id)
        chat_avatar_path = chat_avatar_service.get_avatar_path(chat)

        logger.debug(
            "Current user: %s is going into chat: %s, and all users in this chat are: %s, chat.is_private?= %s, is_user_in_chat? %s, unread_count=%s, user_chats=%s",
            user,
            chat,
            chat_users,
            chat.is_private,
            user_in_chat,
            unread_count,
            user_chats,
        )

        return render_template(
            "chat/chat.html",
            users=chat_users,
            chat=chat,
            user_inchat=user_in_chat,
            user_chats=user_chats,
            unread_count=unread_count,
            chat_avatar_path=chat_avatar_path,
        )

    @socketio.on("send_message_in_chat")
    @csrf.exempt
    def handle_chat_message_sending(data):
        logger.debug("Handling sent message: %s", data)
        # user_id = int(data.get('user_id')) #NOT NEEDED
        chat_id = int(data.get("chat_id"))
        text = str(data.get("text"))

        try:
            message = message_service.create_message(text, g.current_user.id, chat_id)
            emit("new_message", message, room=chat_service.get_chat_url(chat_id))

            for participant in chat_service.get_chat_users(chat_id):
                if participant.id != g.current_user.id:
                    unread_count = message_service.get_unread_count(
                        chat_id, participant.id
                    )
                    emit(
                        "update_unread_count",
                        {"user_id": participant.id, "unread_count": unread_count},
                        room=chat_service.get_chat_url(chat_id),
                    )

        except Exception as e:
            logger.error("Error while handling message: %s", str(e), exc_info=True)
            emit("error", {"message": "An error occurred while sending the message"})

    @app.route("/load-chat-messages-feed", methods=["GET"])
    def load_chat_messages_feed():
        logger.debug("Loading chat messages feed...")
        user_id = session.get("user_id")
        chat_id = request.args.get("chat_id")
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 20))

        try:
            messages = message_service.get_chat_messages(
                chat_id, offset, limit, user_id
            )
            return jsonify({"messages": messages})
        except Exception as e:
            logger.error("Error loading chat messages feed: %s", str(e), exc_info=True)
            return jsonify({"messages": [], "error": str(e)}), 500

    @app.route("/message/<int:message_id>/view", methods=["POST"])
    def view_message(message_id):
        data = request.get_json()
        # user_id = data.get('user_id') #NOT NEEDED ?

        try:
            message = message_service.mark_as_viewed(message_id, g.current_user.id)
            return jsonify({"status": "success", "views": message.views})
        except Exception as e:
            logger.error("Error marking message as viewed: %s", str(e), exc_info=True)
            return jsonify({"status": "error", "message": str(e)}), 500

    @socketio.on("join")
    def on_join(data):
        username = data["username"]
        room = data["room"]
        join_room(room)
        emit("status", {"msg": f"{username} has entered the room."}, room=room)

    @socketio.on("leave")
    def on_leave(data):
        username = data["username"]
        room = data["room"]
        leave_room(room)
        emit("status", {"msg": f"{username} has left the room."}, room=room)
