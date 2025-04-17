import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from flask_app.chat.message.dtos import MessageDTO
from flask_app.user.chat_user.dtos import ChatUserDTO

from ..dtos import ChatDTO


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class ChatService:
    def __init__(self, chat_repo, chat_user_repo, message_repo):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)

    def _validate_chat_user_data(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime]
    ) -> None:
        """Validates the data for creating a chat user."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("user_id must be a positive integer")
        if not isinstance(chat_id, int) or chat_id <= 0:
            raise ValidationError(
                f"chat_id must be a positive integer, chat id is: {chat_id}"
            )

    def _validate_chat_data(
        self, title: str, url_name: str, is_private: bool, description: str
    ) -> None:
        """Validates the data for creating a chat."""
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("title must be a non-empty string")
        if not isinstance(url_name, str) or not url_name.strip():
            raise ValidationError("url_name must be a non-empty string")
        if not isinstance(is_private, bool):
            raise ValidationError("is_private must be a boolean")
        if not isinstance(description, str):
            raise ValidationError("description must be a string")

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> Optional[ChatUserDTO]:
        """Creates a new chat user."""
        self._validate_chat_user_data(user_id, chat_id, muted_until)
        chat_user_data = {
            "user_id": user_id,
            "chat_id": chat_id,
            "muted_until": muted_until,
        }
        try:
            new_chat_user_dto = ChatUserDTO(**chat_user_data)
            return self.chat_user_repo.save(new_chat_user_dto)
        except ValidationError as e:
            self.logger.error(f"Validation error creating chat user: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error creating chat user: {e}")
            raise

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> Optional[ChatDTO]:
        """Creates a new chat."""
        self._validate_chat_data(title, url_name, is_private, description)
        chat_data = {
            "title": title,
            "url_name": url_name,
            "is_private": is_private,
            "description": description,
        }
        try:
            new_chat_dto = ChatDTO(**chat_data)
            return self.chat_repo.save(new_chat_dto)
        except ValidationError as e:
            self.logger.error(f"Validation error creating chat: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error creating chat: {e}")
            raise

    def create_direct_chat(
        self, user1_id: int, user2_id: int, title: str
    ) -> Optional[ChatDTO]:
        """Creates a direct chat between two users."""
        url_name = self._generate_url_name(user1_id, user2_id)
        chat_dto = self.create_chat(title, url_name, is_private=True)
        print(chat_dto)
        if chat_dto is None:
            return None

        self.create_chat_user(user1_id, chat_dto.id)
        self.create_chat_user(user2_id, chat_dto.id)
        return chat_dto

    def _generate_url_name(self, user1_id: int, user2_id: int) -> str:
        """Generates a unique URL name for the chat."""
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[ChatDTO]:
        """Retrieves chat information based on user IDs."""
        url_name = self._generate_url_name(user1_id, user2_id)
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_by_url(self, url_name: str) -> Optional[ChatDTO]:
        """Retrieves chat information by URL name."""
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_users(self, chat_id: int) -> List[ChatUserDTO]:
        """Retrieves users associated with a given chat."""
        return self.chat_repo.get_chat_users(chat_id)

    def get_chat_url(self, chat_id: int) -> Optional[str]:
        """Returns the URL of the chat based on chat ID."""
        chat_dto = self.get_chat_by_id(chat_id)
        return chat_dto.url_name if chat_dto else None

    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        """Retrieves chat information by chat ID."""
        return self.chat_repo.get(chat_id)

    def add_user_to_chat(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> Optional[ChatUserDTO]:
        """Adds a user to a chat."""
        return self.create_chat_user(user_id, chat_id, muted_until)

    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUserDTO]:
        """Approves a user to join the chat."""
        return self.create_chat_user(user_id, chat_id)

    def remove_user_from_chat(self, user_id: int, chat_id: int) -> bool:
        """Removes a user from the chat."""
        return self.chat_user_repo.delete_chat_user(user_id, chat_id)

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Checks if a user is in the chat."""
        return self.chat_user_repo.get_chat_user(user_id, chat_id) is not None

    def get_all_chats(self) -> List[ChatDTO]:
        """Retrieves all chats."""
        return self.chat_repo.get_all()

    def get_user_chats(self, user_id: int) -> List[ChatDTO]:
        """Retrieves all chats for a specific user."""
        return self.chat_user_repo.get_user_chats(user_id)

    def accept_join_request(self, message_id: int) -> str:
        """Accepts a join request from a user."""
        message_dto = self.message_repo.get(message_id)
        if not message_dto:
            return "Request not found"

        if not self.create_chat_user(message_dto.user_id, message_dto.chat_id):
            return "Failed to add user to chat"

        self.message_repo.delete(message_id)
        return f"User {message_dto.user_id} was added to chat"

    def reject_join_request(self, message_id: int) -> str:
        """Rejects a join request from a user."""
        message_dto = self.message_repo.get(message_id)
        if not message_dto:
            return "Request not found"

        self.message_repo.delete(message_id)
        return f"Request from user {message_dto.user_id} was rejected"
