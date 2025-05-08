import logging
from typing import Optional, Tuple


from flask_app.user.exceptions import UserNotFoundError

from ..dtos import UserDTO

# Initialize logger for the module
logger = logging.getLogger(__name__)


class ProfileController:
    """Controller for managing user profiles."""

    def __init__(self, profile_service, avatar_service, user_repo, chat_user_repo):
        self.user_repo = user_repo
        self.chat_user_repo = chat_user_repo
        self.profile_service = profile_service
        self.avatar_service = avatar_service

    def edit_account(self, user_id: int, new_username: str) -> Tuple[str, int]:
        """Edit user account information."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        try:
            self.profile_service.update_username(user_dto, new_username)
            return "Username updated successfully", 200
        except ValueError as e:
            logger.warning(f"Failed to update username for user {user_id}: {e}")
            return str(e), 400

    def get_profile(self, user_id: int) -> Tuple[Optional[UserDTO], int]:
        """Retrieve user profile."""
        user_dto = self.user_repo.get(user_id)

        if user_dto is None:
            logger.info(f"User with id {user_id} not found.")
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        # Update avatar path
        user_dto.avatar_path = self.avatar_service.get_user_avatar_or_generate(user_dto)
        return user_dto, 200

    def update_user_description(
        self, user_id: int, description: str
    ) -> Tuple[str, int]:
        """Update user description."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            logger.info(f"User with id {user_id} not found.")
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        user_dto.description = description
        try:
            self.user_repo.update(user_dto)
            return "Description updated successfully", 200
        except Exception as e:
            logger.error(f"Error updating description for user {user_id}: {e}")
            return str(e), 500

    def update_avatar(self, user_id: int, file) -> Tuple[str, int]:
        """Update user avatar."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        try:
            avatar_path = self.avatar_service.set_avatar(user_dto, file)
            return avatar_path
        except Exception as e:
            logger.error(f"Error updating avatar for user {user_dto.id}: {e}")
            return str(e), 500

    def get_user_description(self, user_id: int) -> Tuple[Optional[str], int]:
        """Retrieve user description."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            logger.info(f"User with id {user_id} not found.")
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        return user_dto.description, 200

    def count_user_posts(self, user_id: int) -> int:
        """Count the number of posts from the user."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        return self.user_repo.count_user_posts(user_dto.id)

    def get_user_chats(self, user_id: int) -> list:
        """Retrieve user chats."""
        user_dto = self.user_repo.get(user_id)
        if user_dto is None:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

        return self.chat_user_repo.get_user_chats(user_dto.id)
