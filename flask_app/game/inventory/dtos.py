from dataclasses import dataclass
from typing import Optional


@dataclass
class InventoryItemDTO:
    id: Optional[int] = None
    user_id: int = 0
    store_item_id: int = 0
    quantity: int = 1
    name: str = ""
    image_path: str = ""
