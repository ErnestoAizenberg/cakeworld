from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NotificationDTO:
    id: Optional[int] = None
    user_id: Optional[int] = None
    message: Optional[str] = None
    type: Optional[str] = None
    is_read: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
