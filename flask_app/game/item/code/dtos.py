from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class ItemCodeDTO:
    id: Optional[int] = None
    inventory_item_id: Optional[int] = None
    user_id: Optional[int] = None
    password_hash: str = ""
    created_at: Optional[datetime] = None
    is_used: Optional[bool] = None
