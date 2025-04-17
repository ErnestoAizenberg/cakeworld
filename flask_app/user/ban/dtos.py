from dataclasses import dataclass
from datetime import datetime


@dataclass
class BannedUserDTO:
    id: int = None
    user_id: str = None
    created: datetime = None
    ban_until: datetime = None
    reason: str = None
    ban_type: str = None  # Например, "post_publication", "reply_to_post"

    def is_banned(self) -> bool:
        """Проверяет, активен ли бан."""
        return self.ban_until > datetime.utcnow()
