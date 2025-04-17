from typing import Any, Optional

from .models import User
from .repositories import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        # Инициализация репозитория пользователя
        self.user_repo = user_repo

    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        return self.user_repo.get(user_id)

    def update_username(self, user_id: int, new_username: str) -> Optional[User]:
        """Обновить имя пользователя."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        existing_user = self.user_repo.get_user_by_username(new_username)
        if existing_user and existing_user.id != user.id:
            raise ValueError("Username already exists")

        user.set_username(new_username)
        self.user_repo.save(user)
        return user

    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя."""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.delete(user)

    def create_user(self, username: str, other_data: Any) -> User:
        """Создать нового пользователя."""
        user = User(
            username=username, other_data=other_data
        )  # Создание нового экземпляра User
        return self.user_repo.save(user)
