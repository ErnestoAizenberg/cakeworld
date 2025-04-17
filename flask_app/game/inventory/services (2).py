import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from .dtos import InventoryItemDTO
from .models import InventoryItem
from .repositories import InventoryItemRepository

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InventoryItemService:
    def __init__(self, repository: InventoryItemRepository):
        self.repository = repository

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
