# flask_app/controllers/ban_controller.py
from typing import Dict, List


class BanController:
    def __init__(self, ban_service: "BanService"):
        self.ban_service = ban_service

    def ban_user(
        self, user_id: str, reason: str, ban_duration_days: int, ban_type: str
    ) -> Dict[str, str]:
        """Забанить пользователя."""
        ban_dto = self.ban_service.ban_user(
            user_id, reason, ban_duration_days, ban_type
        )
        return {"success": f"Пользователь {user_id} забанен до {ban_dto.ban_until}."}

    def unban_user(self, ban_id: int) -> Dict[str, str]:
        """Снять бан."""
        if self.ban_service.unban_user(ban_id):
            return {"success": "Пользователь разблокирован."}
        return {"error": "Бан не найден."}

    def get_banned_users(self) -> List[Dict[str, str]]:
        """Получить список всех забаненных пользователей."""
        bans = self.ban_service.get_active_bans()
        return [
            {
                "user_id": ban.user_id,
                "ban_until": ban.ban_until.isoformat(),
                "reason": ban.reason,
                "ban_type": ban.ban_type,
            }
            for ban in bans
        ]

    def check_ban(self, user_id: str, ban_type: str) -> Dict[str, str]:
        """Проверить, есть ли активный бан для пользователя."""
        if self.ban_service.is_user_banned(user_id):
            return {"error": "Доступ запрещен."}
        return {"success": "Доступ разрешен."}
