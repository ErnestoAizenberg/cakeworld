import logging
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

logger = logging.getLogger(__name__)


def configure_store_item_service_api(app: Flask, service: "StoreItemService"):

    @app.route("/store-items/<int:item_id>", methods=["GET"])
    def get_store_item(item_id: int) -> Dict[str, Any]:
        """Get a store item by ID."""
        logger.debug(f"GET store-item request for ID: {item_id}")
        item = service.get_item(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"item": item.dict()}), 200

    @app.route("/store-items", methods=["POST"])
    def create_store_item() -> Dict[str, Any]:
        """Create a new store item."""
        logger.debug("POST store-item request")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        try:
            item_dto = StoreItemDTO(**data)
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": "Validation failed", "details": str(e)}), 400

        try:
            created_item = service.create_item(data)
            return (
                jsonify(
                    {
                        "message": "Item created successfully",
                        "item_id": created_item.id,
                        "item": created_item.dict(),
                    }
                ),
                201,
            )
        except Exception as e:
            logger.error(f"Error creating item: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/store-items/<int:item_id>", methods=["PUT"])
    def update_store_item(item_id: int) -> Dict[str, Any]:
        """Update an existing store item."""
        logger.debug(f"PUT store-item request for ID: {item_id}")
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        data["id"] = item_id
        try:
            item_dto = StoreItemDTO(**data)
        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            return jsonify({"error": "Validation failed", "details": str(e)}), 400

        updated_item = service.update_item(item_id, data)
        if not updated_item:
            return jsonify({"error": "Item not found"}), 404

        return (
            jsonify(
                {"message": "Item updated successfully", "item": updated_item.dict()}
            ),
            200,
        )

    @app.route("/store-items/<int:item_id>", methods=["DELETE"])
    def delete_store_item(item_id: int) -> Dict[str, Any]:
        """Delete a store item by ID."""
        logger.debug(f"DELETE store-item request for ID: {item_id}")
        success = service.delete_item(item_id)
        if not success:
            return jsonify({"error": "Item not found"}), 404

        return jsonify({"message": "Item deleted successfully"}), 200

    @app.route("/store-items", methods=["GET"])
    def get_all_store_items() -> Dict[str, Any]:
        """Get all store items."""
        logger.debug("GET all store-items request")
        try:
            items = service.get_all_items()
            return jsonify([item.dict() for item in items]), 200
        except Exception as e:
            logger.error(f"Error getting items: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/store-items/template", methods=["GET"])
    def store_item_template() -> str:
        """Render the store item folder template."""
        logger.debug("Rendering store item folder template")
        return render_template("store_item_folder.html")
