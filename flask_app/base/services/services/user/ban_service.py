from datetime import datetime, timedelta
from typing import List, Optional

from .models import BannedUser, ChatUser


class BanService:
    def __init__(self, banned_user_repo):
        self.banned_user_repo = banned_user_repo

    def ban_user(
        self, user_id: str, reason: str, ban_duration_days: int, ban_type: str
    ) -> BannedUser:
        """Забанить пользователя на указанное количество дней."""
        ban_until = datetime.utcnow() + timedelta(days=ban_duration_days)
        return self.banned_user_repo.save(
            BannedUser(
                user_id=user_id, reason=reason, ban_until=ban_until, ban_type=ban_type
            )
        )

    def update_ban(
        self, ban_id: int, reason: str, ban_duration_days: int
    ) -> Optional[BannedUser]:
        """Обновить бан (например, изменить причину или срок)."""
        ban_until = datetime.utcnow() + timedelta(days=ban_duration_days)
        ban = self.banned_user_repo.get(ban_id)
        if ban:
            ban.reason = reason
            ban.ban_until = ban_until
            return self.banned_user_repo.update(ban)
        return None

    def unban_user(self, ban_id: int) -> bool:
        """Снять бан."""
        ban = self.banned_user_repo.get(ban_id)
        if ban:
            return self.banned_user_repo.delete(ban)
        return False

    def is_user_banned(self, user_id: str) -> bool:
        """Проверить, есть ли активные баны у пользователя."""
        active_bans = self.banned_user_repo.get_active_bans_by_user_id(user_id)
        return len(active_bans) > 0

    def get_active_bans(self, user_id: str) -> List[BannedUser]:
        """Получить все активные баны для пользователя."""
        return self.banned_user_repo.get_active_bans_by_user_id(user_id)
