# chat/direct/services.py
from typing import Optional

from ..message.services import MessageService
from ..public.services import ChatService


class DirectChatService:
    """Service for direct chat operations between two users."""

    def __init__(self, chat_service: ChatService, message_service: MessageService):
        self.chat_service = chat_service
        self.message_service = message_service

    def get_or_create_direct_chat(self, user1_id: int, user2_id: int):
        """Get or create a direct chat between two users."""
        chat = self.chat_service.get_chat_by_users(user1_id, user2_id)
        print(chat)
        if not chat:
            print("Creating direct chat...")
            chat = self.chat_service.create_direct_chat(
                user1_id=user1_id,
                user2_id=user2_id,
                title=f"Chat between {user1_id} and {user2_id}",
            )
        return chat

    def send_direct_message(self, chat_id: int, author_id: int, text: str) -> dict:
        """Send a message in a direct chat."""
        # Validate user is part of the chat
        if not self.chat_service.is_user_in_chat(chat_id, author_id):
            raise ValueError("User is not part of this chat")

        return self.message_service.create_message(
            text=text, user_id=author_id, chat_id=chat_id
        )

    def get_direct_messages(
        self, chat_id: int, user_id: int, limit: int = 20, offset: int = 0
    ) -> list:
        """Get messages from a direct chat."""
        if not self.chat_service.is_user_in_chat(chat_id, user_id):
            raise ValueError("User is not part of this chat")

        return self.message_service.get_chat_messages(chat_id, offset, limit)

    def mark_direct_message_read(
        self, message_id: int, reader_id: int
    ) -> Optional[dict]:
        """Mark a direct message as read."""
        message = self.message_service.get_message(message_id)
        if not message or not self.chat_service.is_user_in_chat(
            message.chat_id, reader_id
        ):
            return None

        return self.message_service.mark_as_viewed(message_id, reader_id)
