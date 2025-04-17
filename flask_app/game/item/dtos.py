from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class StoreItemDTO:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    price_coins: Optional[int] = None
    price_gems: Optional[int] = None
    image_path: str = ""
    rarity: int = field(default=0)
