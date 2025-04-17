from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ChatUserDTO:
    chat_id: int
    user_id: int
    muted_until: Optional[datetime] = None
