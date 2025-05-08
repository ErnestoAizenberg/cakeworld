from flask import jsonify, request


from .services import PrayerService


def configure_pray_routes(app, prayer_service: PrayerService):
    @app.route("/prayer", methods=["POST"])
    def perform_prayer():
        data = request.get_json()
        user_id = data.get("user_id")
        banner_id = data.get("banner_id")

        if not user_id or not banner_id:
            return jsonify({"error": "Invalid request"}), 400

        try:
            item_code = prayer_service.perform_prayer(user_id, banner_id)
            if item_code:
                return (
                    jsonify(
                        {
                            "success": True,
                            "item_code": {
                                "id": item_code.id,
                                "code": item_code.code,
                                "item_name": item_code.item_name,
                            },
                        }
                    ),
                    200,
                )
            else:
                return (
                    jsonify(
                        {"success": True, "message": "No item code won this time."}
                    ),
                    200,
                )

        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception:
            return jsonify({"error": "Internal server error"}), 500
