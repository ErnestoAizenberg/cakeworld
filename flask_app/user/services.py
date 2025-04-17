from typing import Any, Optional

from .dtos import UserDTO
from .exceptions import UserNotFoundError


class UserService:
    def __init__(
        self,
        user_repo: "UserRepository",
    ):
        self.user_repo = user_repo

    def get_user_chats(self, user_id):
        self.user_repo.get_user_chats(user_id)

    def get_user(self, user_id: int) -> Optional["UserDTO"]:
        """Получить пользователя по ID."""
        user_dto = self.user_repo.get(user_id)
        if user_dto:
            return user_dto
        else:
            raise UserNotFoundError(f"User with the id: {user_id} is not found")
            return None

    def create_user(self, username: str, email: str, password: str) -> "UserDTO":
        """Создать нового пользователя."""
        user_dto = UserDTO(username=username, other_data=other_data)
        return self.save_user(user_dto)

    def save_user(self, user_dto: UserDTO) -> UserDTO:
        """Сохранить пользователя"""
        return self.user_repo.save(user_dto)

    def get_all_users(self) -> list[UserDTO]:
        """Получить всех пользователей"""
        return self.user_repo.get_all()

    def get_user_by_email(self, email) -> UserDTO:
        user_dto = self.user_repo.get_user_by_email(email)
        return user_dto

    def get_user_by_username(self, username):
        user_dto = self.user_repo.get_user_by_username(username)
        return user_dto

    def delete_user(self, user_id: int) -> None:
        """Удалить пользователя."""
        user = self.user_repo.get(user_id)
        if not user:
            raise UserNotFoundError(f"User with id {user_id} not found")
        self.user_repo.delete(user)

    def count_user_posts(self, user_id: int) -> int:
        """Count the number of posts for a given user."""
        return self.user_repo.count_user_posts(user_id)
