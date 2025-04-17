from datetime import datetime
from typing import List, Optional

from flask_app.chat.message.dtos import MessageDTO
from flask_app.user.chat_user.dtos import ChatUserDTO

from ..dtos import ChatDTO


class ChatService:
    def __init__(self, chat_repo, chat_user_repo, message_repo):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo
        self.message_repo = message_repo

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUserDTO:
        """Создает нового участника чата и возвращает DTO"""
        chat_user_data = {
            "user_id": user_id,
            "chat_id": chat_id,
            "muted_until": muted_until,
        }
        # IMPLEMENT DATA VALIDATION
        new_chat_user_dto = ChatUserDTO(**chat_user_data)
        chat_user_dto = self.chat_user_repo.save(new_chat_user_dto)
        # IMPLEMENT ERROR HANDLING
        return chat_user_dto

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> ChatDTO:
        """Создает новый чат и возвращает DTO"""
        chat_data = {
            "title": title,
            "url_name": url_name,
            "is_private": is_private,
            "description": description,
        }
        new_chat_dto = ChatDTO(**chat_data)
        saved_dto = self.chat_repo.save(new_chat_dto)
        if saved_dto:
            return saved_dto
        else:
            raise ValueError("Error during creating chat")

    def create_direct_chat(self, user1_id: int, user2_id: int, title: str) -> ChatDTO:
        """Создает директ чат между двумя пользователями и возвращает DTO"""
        url_name = self._generate_url_name(user1_id, user2_id)
        chat_dto = self.create_chat(title, url_name, is_private=True)
        self.create_chat_user(user1_id, chat_dto.id)
        self.create_chat_user(user2_id, chat_dto.id)
        return chat_dto

    def _generate_url_name(self, user1_id: int, user2_id: int) -> str:
        """Генерирует уникальное имя URL для директ чата"""
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[ChatDTO]:
        """Получить директ чат между двумя пользователями как DTO"""
        url_name = self._generate_url_name(user1_id, user2_id)
        chat_data = self.chat_repo.get_chat_by_url(url_name)
        return ChatDTO(**chat_data) if chat_data else None

    def get_chat_by_url(self, url_name: str) -> Optional[ChatDTO]:
        """Получить чат по URL как DTO"""
        chat_data = self.chat_repo.get_chat_by_url(url_name)
        return ChatDTO(**chat_data) if chat_data else None

    def get_chat_users(self, chat_id: int) -> List[ChatUserDTO]:
        """Получить всех участников чата как список DTO"""
        users_data = self.chat_repo.get_chat_users(chat_id)
        return [ChatUserDTO(**user_data) for user_data in users_data]

    def get_chat_url(self, chat_id: int) -> Optional[str]:
        """Получить URL чата"""
        chat_dto = self.get_chat_by_id(chat_id)
        return chat_dto.url_name if chat_dto else None

    def get_chat_by_id(self, chat_id: int) -> Optional[ChatDTO]:
        """Получить чат по ID как DTO"""
        chat_data = self.chat_repo.get(chat_id)
        return ChatDTO(**chat_data) if chat_data else None

    def add_user_to_chat(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUserDTO:
        """Добавить пользователя в чат и вернуть DTO"""
        return self.create_chat_user(user_id, chat_id, muted_until)

    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUserDTO]:
        """Одобрить пользователя в чате и вернуть DTO"""
        return self.create_chat_user(user_id, chat_id)

    def remove_user_from_chat(self, user_id: int, chat_id: int) -> bool:
        """Удалить пользователя из чата"""
        return self.chat_user_repo.delete_chat_user(user_id, chat_id)

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Проверить, находится ли пользователь в чате"""
        return self.chat_user_repo.get_chat_user(user_id, chat_id) is not None

    def get_user_chats(self, user_id: int) -> List[ChatDTO]:
        """Получить все чаты пользователя как список DTO"""
        chats_data = self.chat_user_repo.get_user_chats(user_id)
        return [ChatDTO(**chat_data) for chat_data in chats_data]

    def accept_join_request(self, message_id: int) -> str:
        """Принять запрос на присоединение к чату"""
        message_data = self.message_repo.get(message_id)
        if not message_data:
            return "Запрос не найден"

        message = MessageDTO(**message_data)
        chat_user_dto = self.create_chat_user(message.user_id, message.chat_id)
        self.message_repo.delete(message_id)

        return f"Пользователь {message.user_id} был добавлен в чат"

    def reject_join_request(self, message_id: int) -> str:
        """Отклонить запрос на присоединение к чату"""
        message_data = self.message_repo.get(message_id)
        if not message_data:
            return "Запрос не найден"

        self.message_repo.delete(message_id)
        return f"Запрос пользователя {message_data['user_id']} был отклонен"
