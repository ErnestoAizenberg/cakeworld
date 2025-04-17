import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from flask_app.chat.message.dtos import MessageDTO
from flask_app.user.chat_user.dtos import ChatUserDTO

from ..dtos import ChatDTO


class ChatServiceError(Exception):
    """Base exception for chat service errors."""

    pass


class ValidationError(ChatServiceError):
    """Exception for validation errors."""

    pass


class ChatCreationError(ChatServiceError):
    """Exception for chat creation failures."""

    pass


class ChatUserCreationError(ChatServiceError):
    """Exception for chat user creation failures."""

    pass


class ChatService:
    def __init__(self, chat_repo, chat_user_repo, message_repo):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)

    def _validate_chat_user_data(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> None:
        """Validates chat user data before creation."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("Invalid user_id: must be positive integer")
        if not isinstance(chat_id, int) or chat_id <= 0:
            raise ValidationError("Invalid chat_id: must be positive integer")
        if muted_until and not isinstance(muted_until, datetime):
            raise ValidationError("Invalid muted_until: must be datetime or None")

    def _validate_chat_data(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> None:
        """Validates chat data before creation."""
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Invalid title: must be non-empty string")
        if not isinstance(url_name, str) or not url_name.strip():
            raise ValidationError("Invalid url_name: must be non-empty string")
        if not isinstance(is_private, bool):
            raise ValidationError("Invalid is_private: must be boolean")
        if not isinstance(description, str):
            raise ValidationError("Invalid description: must be string")

    def _generate_direct_chat_url(self, user1_id: int, user2_id: int) -> str:
        """Generates consistent URL name for direct chats."""
        if not all(isinstance(i, int) and i > 0 for i in (user1_id, user2_id)):
            raise ValidationError("User IDs must be positive integers")
        return f"direct_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUserDTO:
        """Creates a new chat user relationship.

        Args:
            user_id: ID of the user to add
            chat_id: ID of the chat to add to
            muted_until: Optional mute expiration datetime

        Returns:
            Created ChatUserDTO

        Raises:
            ChatUserCreationError: If creation fails
        """
        try:
            self._validate_chat_user_data(user_id, chat_id, muted_until)

            chat_user_dto = ChatUserDTO(
                user_id=user_id, chat_id=chat_id, muted_until=muted_until
            )

            created = self.chat_user_repo.save(chat_user_dto)
            if not created:
                raise ChatUserCreationError("Failed to create chat user")

            return created

        except Exception as e:
            self.logger.error(f"Failed to create chat user: {str(e)}")
            raise ChatUserCreationError(f"Could not create chat user: {str(e)}")

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> ChatDTO:
        """Creates a new chat.

        Args:
            title: Chat display name
            url_name: Unique URL identifier
            is_private: Whether chat is private
            description: Optional chat description

        Returns:
            Created ChatDTO

        Raises:
            ChatCreationError: If creation fails
        """
        try:
            self._validate_chat_data(title, url_name, is_private, description)

            chat_dto = ChatDTO(
                title=title,
                url_name=url_name,
                is_private=is_private,
                description=description,
            )

            created = self.chat_repo.save(chat_dto)
            if not created:
                raise ChatCreationError("Failed to create chat")

            return created

        except Exception as e:
            self.logger.error(f"Failed to create chat: {str(e)}")
            raise ChatCreationError(f"Could not create chat: {str(e)}")

    def create_direct_chat(
        self, user1_id: int, user2_id: int, title: str = None
    ) -> ChatDTO:
        """Creates a direct chat between two users with automatic ChatUser creation.

        Args:
            user1_id: First user ID
            user2_id: Second user ID
            title: Optional custom title (defaults to "User1 & User2")

        Returns:
            Created ChatDTO

        Raises:
            ChatCreationError: If any step fails
        """
        try:
            # Validate input
            if user1_id == user2_id:
                raise ValidationError("Cannot create direct chat with same user")

            # Generate consistent URL name
            url_name = self._generate_direct_chat_url(user1_id, user2_id)

            # Check if chat already exists
            existing_chat = self.chat_repo.get_chat_by_url(url_name)
            if existing_chat:
                return existing_chat

            # Create default title if none provided
            if not title:
                user1 = f"User-{user1_id}"
                user2 = f"User-{user2_id}"
                title = f"{user1} & {user2}"

            # Create the chat
            chat_dto = self.create_chat(title=title, url_name=url_name, is_private=True)

            # Add both users to the chat
            self.create_chat_user(user1_id, chat_dto.id)
            self.create_chat_user(user2_id, chat_dto.id)

            return chat_dto

        except Exception as e:
            self.logger.error(f"Failed to create direct chat: {str(e)}")
            raise ChatCreationError(f"Could not create direct chat: {str(e)}")

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[ChatDTO]:
        """Finds direct chat between two users."""
        try:
            url_name = self._generate_direct_chat_url(user1_id, user2_id)
            return self.chat_repo.get_chat_by_url(url_name)
        except Exception as e:
            self.logger.error(f"Error finding chat by users: {str(e)}")
            return None

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Checks if user is in chat."""
        try:
            return bool(self.chat_user_repo.get_chat_user(user_id, chat_id))
        except Exception as e:
            self.logger.error(f"Error checking user in chat: {str(e)}")
            return False

    def get_user_chats(self, user_id: int) -> List[ChatDTO]:
        """Gets all chats for a user."""
        try:
            return self.chat_user_repo.get_user_chats(user_id) or []
        except Exception as e:
            self.logger.error(f"Error getting user chats: {str(e)}")
            return []

    # ... (keep other methods with similar error handling improvements)

    def accept_join_request(self, message_id: int) -> Tuple[bool, str]:
        """Processes a join request acceptance.

        Returns:
            Tuple of (success, message)
        """
        try:
            message_dto = self.message_repo.get(message_id)
            if not message_dto:
                return False, "Request not found"

            if not self.create_chat_user(message_dto.user_id, message_dto.chat_id):
                return False, "Failed to add user to chat"

            self.message_repo.delete(message_id)
            return True, f"User {message_dto.user_id} added to chat"

        except Exception as e:
            self.logger.error(f"Error accepting join request: {str(e)}")
            return False, f"Error processing request: {str(e)}"
