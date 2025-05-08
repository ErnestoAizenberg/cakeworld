from flask import Blueprint, jsonify, request, session

ban_bp = Blueprint("ban", __name__)


def configure_ban_routes(app, ban_controller):
    @ban_bp.route("/ban_user", methods=["POST"])
    def ban_user():
        user_id = request.form["user_id"]
        ban_duration = int(request.form["ban_duration"])
        reason = request.form["reason"]
        ban_type = request.form["ban_type"]

        result = ban_controller.ban_user(user_id, reason, ban_duration, ban_type)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 201

    @ban_bp.route("/unban_user/<int:ban_id>", methods=["DELETE"])
    def unban_user(ban_id):
        result = ban_controller.unban_user(ban_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200

    @ban_bp.route("/banned_users", methods=["GET"])
    def banned_users():
        result = ban_controller.get_banned_users()
        return jsonify(result), 200

    @ban_bp.route("/check_ban/<ban_type>", methods=["GET"])
    def check_ban(ban_type):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Необходима аутентификация."}), 401

        result = ban_controller.check_ban(user_id, ban_type)
        if "error" in result:
            return jsonify(result), 403
        return jsonify(result), 200

    app.register_blueprint(ban_bp)
