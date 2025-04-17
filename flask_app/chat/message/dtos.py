# chat/message/dtos.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class MessageDTO:
    """Data Transfer Object for Message entities."""

    id: Optional[int] = None
    text: Optional[str] = None
    user_id: Optional[int] = None
    chat_id: Optional[int] = None
    created: Optional[datetime] = datetime.utcnow
    images: Optional[List[str]] = field(default_factory=list)
    views: Optional[List[int]] = field(default_factory=list)
