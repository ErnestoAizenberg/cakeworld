# flask_app/controllers/message_reaction_controller.py
from flask import jsonify, request


class MessageReactionController:
    def __init__(self, reaction_service: "ReactionService"):
        self.reaction_service = reaction_service

    def get_reactions(self, message_id: int):
        """Get all reactions for a specific message."""
        try:
            reactions = self.reaction_service.get_reactions(message_id)
            return (
                jsonify(
                    {
                        "status": "success",
                        "message_id": message_id,
                        "reactions": reactions,
                    }
                ),
                200,
            )
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    def react_to_message(self):
        """Add or update a reaction to a message."""
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            message_id = data.get("message_id")
            emoji = data.get("emoji")

            if not all([user_id, message_id, emoji]):
                return (
                    jsonify({"status": "error", "message": "Missing required fields"}),
                    400,
                )

            self.reaction_service.react_to_message(user_id, message_id, emoji)
            return jsonify({"status": "success", "message": "Reaction updated"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
