from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class InventoryItemDTO:
    id: Optional[int] = None
    user_id: int = 0
    store_item_id: int = 0
    quantity: int = 1
    name: str = ""
    image_path: str = ""
