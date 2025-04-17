from datetime import datetime
from typing import List, Optional

from .models import Chat, ChatUser, Message, User
from .repositories import ChatRepository, ChatUserRepository, MessageRepository


class ChatService:
    def __init__(self):
        self.chat_repo = ChatRepository()
        self.chat_user_repo = ChatUserRepository()
        self.message_repo = MessageRepository()

    # Методы работы с чатами
    def get_chat_by_url(self, url_name: str):
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_users(self, chat_id: int):
        return self.chat_user_repo.get_user_chats(chat_id)

    def get_chat_url(self, chat_id: int):
        chat = self.chat_repo.get(chat_id)
        return chat.url_name if chat else None

    def get_chat_by_users(self, user1_id: int, user2_id: int):
        """Получить чат между двумя пользователями."""
        return self.chat_repo.get_chat_by_users(user1_id, user2_id)

    def create_chat(self, title: str, is_private: bool, url_name: str):
        """Создать новый чат и добавить его в репозиторий."""
        chat = Chat(title=title, is_private=is_private, url_name=url_name)
        self.chat_repo.create(chat)  # Метод репозитория для создания чата
        return chat

    def add_user_to_chat(self, user_id: int, chat_id: int):
        """Добавить пользователя в чат."""
        return self.chat_user_repo.create_chat_user(user_id, chat_id)

    # Методы работы с пользователями в чатах
    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUser]:
        """Одобрить пользователя в чате."""
        return self.chat_user_repo.approve_user(user_id, chat_id)

    def add_user_to_chat(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUser:
        """Добавить пользователя в чат."""
        return self.chat_user_repo.create_chat_user(user_id, chat_id, muted_until)

    def remove_user_from_chat(self, user_id: int, chat_id: int) -> bool:
        """Удалить пользователя из чата."""
        return self.chat_user_repo.delete_chat_user(user_id, chat_id)

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Проверить, находится ли пользователь в чате."""
        return self.chat_user_repo.get_chat_user(user_id, chat_id) is not None

    def get_user_chats(self, user_id: int):
        """Получить все чаты, в которых находится пользователь."""
        return self.chat_user_repo.get_user_chats(user_id)

    def accept_join_request(self, message_id: int) -> str:
        """Принять запрос на присоединение пользователя к чату."""
        message = self.message_repo.get(message_id)
        if message:
            joiner = User.query.get(message.user_id)
            chat = self.chat_repo.get(message.chat_id)

            chat.add_user(joiner)  # Метод добавления пользователя в чат
            self.message_repo.delete(message)  # Удаляем сообщение запроса
            return f"Пользователь {joiner.username} был добавлен в чат"
        return "Запрос не найден"

    def reject_join_request(self, message_id: int) -> str:
        """Отклонить запрос на присоединение пользователя к чату."""
        message = self.message_repo.get(message_id)
        if message:
            self.message_repo.delete(message)  # Удаляем сообщение запроса
            return f"Запрос пользователя {message.user_id} был отклонен"
        return "Запрос не найден"
