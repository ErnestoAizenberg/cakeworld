import logging
from datetime import datetime
from typing import List, Optional

from flask_app.chat.message.dtos import MessageDTO
from flask_app.user.chat_user.dtos import ChatUserDTO

from ..dtos import ChatDTO


class ValidationError(Exception):
    pass


class ChatService:
    def __init__(self, chat_repo, chat_user_repo, message_repo):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo
        self.message_repo = message_repo
        self.logger = logging.getLogger(__name__)

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> Optional[ChatUserDTO]:
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
            return None

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> Optional[ChatDTO]:
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
            return None

    def create_direct_chat(
        self, user1_id: int, user2_id: int, title: str
    ) -> Optional[ChatDTO]:
        url_name = self._generate_url_name(user1_id, user2_id)
        chat_dto = self.create_chat(title, url_name, is_private=True)

        if not chat_dto:
            return None

        self.create_chat_user(user1_id, chat_dto.id)
        self.create_chat_user(user2_id, chat_dto.id)
        return chat_dto

    def _generate_url_name(self, user1_id: int, user2_id: int) -> str:
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[ChatDTO]:
        url_name = self._generate_url_name(user1_id, user2_id)
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_by_url(self, url_name: str) -> Optional[ChatDTO]:
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_users(self, chat_id: int) -> List[ChatUserDTO]:
        return self.chat_repo.get_chat_users(chat_id)

    def get_chat_url(self, chat_id: int) -> Optional[str]:
        chat_dto = self.get_chat_by_id(chat_id)
        return chat_dto.url_name if chat_dto else None

    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        return self.chat_repo.get(chat_id)

    def add_user_to_chat(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> Optional[ChatUserDTO]:
        return self.create_chat_user(user_id, chat_id, muted_until)

    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUserDTO]:
        return self.create_chat_user(user_id, chat_id)

    def remove_user_from_chat(self, user_id: int, chat_id: int) -> bool:
        return self.chat_user_repo.delete_chat_user(user_id, chat_id)

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        return self.chat_user_repo.get_chat_user(user_id, chat_id) is not None

    def get_all_chats(self) -> List[ChatDTO]:
        return self.chat_repo.get_all()

    def get_user_chats(self, user_id: int) -> List[ChatDTO]:
        return self.chat_user_repo.get_user_chats(user_id)

    def accept_join_request(self, message_id: int) -> str:
        message_dto = self.message_repo.get(message_id)
        if not message_dto:
            return "Request not found"

        if not self.create_chat_user(message_dto.user_id, message_dto.chat_id):
            return "Failed to add user to chat"

        self.message_repo.delete(message_id)
        return f"User {message_dto.user_id} was added to chat"

    def reject_join_request(self, message_id: int) -> str:
        message_dto = self.message_repo.get(message_id)
        if not message_dto:
            return "Request not found"

        self.message_repo.delete(message_id)
        return f"Request from user {message_dto.user_id} was rejected"
