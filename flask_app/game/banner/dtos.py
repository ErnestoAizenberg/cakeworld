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
