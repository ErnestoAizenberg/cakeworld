import logging

from flask import jsonify, render_template, request

logger = logging.getLogger(__name__)


def configure_store_item_service_api(app, controller):

    @app.route("/store-items/<int:item_id>", methods=["GET"])
    def get_store_item(item_id):
        logger.debug(f"GET store-item request for ID: {item_id}")
        return controller.get_item(item_id)

    @app.route("/store-items", methods=["POST"])
    def create_store_item():
        logger.debug("POST store-item request")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        return controller.create_item(data)

    @app.route("/store-items/<int:item_id>", methods=["PUT"])
    def update_store_item(item_id):
        logger.debug(f"PUT store-item request for ID: {item_id}")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        return controller.update_item(item_id, data)

    @app.route("/store-items/<int:item_id>", methods=["DELETE"])
    def delete_store_item(item_id):
        logger.debug(f"DELETE store-item request for ID: {item_id}")
        return controller.delete_item(item_id)

    @app.route("/store-items", methods=["GET"])
    def get_all_store_items():
        logger.debug("GET all store-items request")
        return controller.get_all_items()

    @app.route("/store-items/template", methods=["GET"])
    def store_item_template():
        logger.debug("Rendering store item folder template")
        return render_template("store_item_folder.html")
