# chat/direct/dtos.py
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class DirectMessageDTO:
    """DTO for direct message details."""

    id: int
    text: str
    created: datetime
    images: List[str]
    is_read: dict

    @classmethod
    def from_message(
        cls, message: "Message", user1_id: int, user2_id: int
    ) -> "DirectMessageDTO":
        """Create DTO from Message model."""
        return cls(
            id=message.id,
            text=message.text,
            created=message.created,
            images=message.images or [],
            is_read={
                "user1": user1_id in (message.views or []),
                "user2": user2_id in (message.views or []),
            },
        )
