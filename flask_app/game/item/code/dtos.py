from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ItemCodeDTO:
    id: Optional[int] = None
    inventory_item_id: Optional[int] = None
    user_id: Optional[int] = None
    password_hash: str = ""
    created_at: Optional[datetime] = None
    is_used: Optional[bool] = None
