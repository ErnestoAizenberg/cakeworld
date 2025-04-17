# flask_app/routes/reaction_routes.py
from flask import Blueprint, jsonify, request


def configure_reaction_routes(app, reaction_controller):
    @app.route("/message/<int:message_id>/reactions", methods=["GET"])
    def get_reactions(message_id: int):
        """Получает все реакции для конкретного сообщения."""
        return reaction_controller.get_reactions(message_id)

    @app.route("/react", methods=["POST"])
    def react_to_message():
        """Добавляет или обновляет реакцию на сообщение."""
        data = request.get_json()
        user_id = data.get("user_id")
        message_id = data.get("message_id")
        emoji = data.get("emoji")

        if not all([user_id, message_id, emoji]):
            return jsonify({"error": "Missing required fields"}), 400

        return reaction_controller.react_to_message(user_id, message_id, emoji)


reaction_bp = Blueprint("reaction", __name__, url_prefix="/api/reactions")


def configure_message_reaction_routes(
    reaction_controller,
):
    @reaction_bp.route("/<int:message_id>", methods=["GET"])
    def get_reactions(message_id):
        return reaction_controller.get_reactions(message_id)

    @reaction_bp.route("", methods=["POST"])
    def react_to_message():
        return reaction_controller.react_to_message()
