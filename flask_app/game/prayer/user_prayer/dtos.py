from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional


@dataclass
class UserPrayDTO:
    id: Optional[int] = None
    user_id: int = 0
    banner_id: int = 0
    created_at: Optional[datetime] = None
