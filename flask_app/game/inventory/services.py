import logging
from typing import List, Optional

from flask_app.game.item.dtos import StoreItemDTO

from .dtos import InventoryItemDTO
from .repositories import InventoryItemRepository

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InventoryItemService:
    def __init__(self, repository: InventoryItemRepository):
        self.repository = repository

    def add_or_update_item(
        self, user_id: int, store_item: StoreItemDTO, quantity: int = 1
    ) -> InventoryItemDTO:
        """
        Add a store item to user's inventory or increase its quantity if already exists.

        :param user_id: ID of the user receiving the item
        :param store_item: StoreItemDTO that user received
        :param quantity: Quantity to add (default 1)
        :return: Created or updated InventoryItemDTO
        """
        # Check if user already has this item in inventory
        inventory = self.get_inventory_by_user_id(user_id)
        existing_item = next(
            (item for item in inventory if item.store_item_id == store_item.id), None
        )

        if existing_item:
            # Update quantity of existing item
            return self.update_item_quantity(
                user_id=user_id, store_item_id=store_item.id, quantity_change=quantity
            )
        else:
            # Create new inventory item
            new_item_data = {
                "user_id": user_id,
                "store_item_id": store_item.id,
                "quantity": quantity,
            }
            return self.create_inventory_item(new_item_data)

    def update_item_quantity(
        self, user_id: int, store_item_id: int, quantity_change: int = 1
    ) -> InventoryItemDTO:
        """
        Update quantity of a specific item in user's inventory.

        :param user_id: ID of the user
        :param store_item_id: ID of the store item to update
        :param quantity_change: Amount to add to current quantity (can be negative)
        :return: Updated InventoryItemDTO
        """
        inventory = self.get_inventory_by_user_id(user_id)
        existing_item = next(
            (item for item in inventory if item.store_item_id == store_item_id), None
        )

        if not existing_item:
            raise ValueError(
                f"Item {store_item_id} not found in user {user_id}'s inventory"
            )

        new_quantity = existing_item.quantity + quantity_change
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")

        update_data = {
            "id": existing_item.id,
            "user_id": user_id,
            "store_item_id": store_item_id,
            "quantity": new_quantity,
        }
        return self.update_inventory_item(existing_item.id, update_data)

    def create_inventory_item(self, item_data: dict) -> InventoryItemDTO:
        """
        Create a new inventory item.

        :param item_data: A dictionary containing the data for the item.
        :return: Created InventoryItemDTO.
        """
        inventory_item_dto = InventoryItemDTO(**item_data)
        logger.info(f"Creating inventory item: {inventory_item_dto}")
        return self.repository.save(inventory_item_dto)

    def get_inventory_item(self, item_id: int) -> Optional[InventoryItemDTO]:
        """
        Retrieve an inventory item by its ID.

        :param item_id: The ID of the inventory item.
        :return: An optional InventoryItemDTO.
        """
        logger.info(f"Retrieving inventory item with id: {item_id}")
        return self.repository.get(item_id)

    def get_inventory_by_user_id(self, user_id: int) -> List[InventoryItemDTO]:
        """
        Retrieve all inventory items for a given user.

        :param user_id: The ID of the user.
        :return: A list of InventoryItemDTOs.
        """
        logger.info(f"Retrieving inventory for user id: {user_id}")
        return self.repository.get_inventory_by_user_id(user_id)

    def update_inventory_item(
        self, item_id: int, item_data: dict
    ) -> Optional[InventoryItemDTO]:
        """
        Update an existing inventory item.

        :param item_id: The ID of the inventory item to update.
        :param item_data: A dictionary containing updated data for the item.
        :return: Updated InventoryItemDTO.
        """
        item_data["id"] = item_id
        inventory_item_dto = InventoryItemDTO(**item_data)
        logger.info(f"Updating inventory item with id: {item_id}")
        return self.repository.update(inventory_item_dto)

    def delete_inventory_item(self, item_id: int) -> bool:
        """
        Delete an inventory item by its ID.

        :param item_id: The ID of the inventory item to delete.
        :return: True if deletion was successful, False otherwise.
        """
        logger.info(f"Deleting inventory item with id: {item_id}")
        return self.repository.delete(item_id)
