from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class BannerDTO:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    icon: str = ""
    created_at: Optional[datetime] = None
    logic: Optional[Dict] = field(default_factory=dict)


@dataclass
class UserPrayDTO:
    id: Optional[int] = None
    user_id: int = 0
    banner_id: int = 0
    created_at: Optional[datetime] = None


@dataclass
class CurrencyDTO:
    id: Optional[int] = None
    user_id: int = 0
    coins: int = 0
    stones: int = 0
    gems: int = 0


@dataclass
class StoreItemDTO:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    price_coins: Optional[int] = None
    price_gems: Optional[int] = None
    image_path: str = ""
    rarity: int = field(default=0)


@dataclass
class InventoryItemDTO:
    id: Optional[int] = None
    user_id: int = 0
    store_item_id: int = 0
    quantity: int = 1
