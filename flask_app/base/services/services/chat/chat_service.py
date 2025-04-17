from datetime import datetime
from typing import List, Optional

from .models import Chat, ChatUser, Message, User
from .repositories import ChatRepository, ChatUserRepository, MessageRepository


class ChatService:
    def __init__(self):
        self.chat_repo = ChatRepository()
        self.chat_user_repo = ChatUserRepository()
        self.message_repo = MessageRepository()

    def create_chat_user(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUser:
        new_chat_user = ChatUser(
            user_id=user_id, chat_id=chat_id, muted_until=muted_until
        )
        return self.chat_repo.save(new_chat_user)

    def create_chat(
        self, title: str, url_name: str, is_private: bool = False, description: str = ""
    ) -> Chat:
        chat = Chat(
            title=title,
            url_name=url_name,
            is_private=is_private,
            description=description,
        )
        return self.chat_repo.save(chat)

    def create_direct_chat(self, user1_id: int, user2_id: int, title: str) -> Chat:
        """Создает директ чат между двумя пользователями."""
        url_name = self._generate_url_name(user1_id, user2_id)
        chat = self.create_chat(title, url_name, is_private=True)
        self.add_user_to_chat(user1_id, chat.id)
        self.add_user_to_chat(user2_id, chat.id)
        return chat

    def _generate_url_name(self, user1_id: int, user2_id: int) -> str:
        """Генерирует уникальное имя URL для директ чата на основании ID пользователей."""
        return f"{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[Chat]:
        """Получить директ чат между двумя пользователями, если он существует."""
        url_name = self._generate_url_name(user1_id, user2_id)
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_by_url(self, url_name: str) -> Optional[Chat]:
        return self.chat_repo.get_chat_by_url(url_name)

    def get_chat_users(self, chat_id: int) -> List[ChatUser]:
        return self.chat_repo.get_chat_users(chat_id)

    def get_chat_url(self, chat_id: int) -> Optional[str]:
        chat = self.chat_repo.get(chat_id)
        return chat.url_name if chat else None

    def add_user_to_chat(
        self, user_id: int, chat_id: int, muted_until: Optional[datetime] = None
    ) -> ChatUser:
        """Добавить пользователя в чат."""
        return self.create_chat_user(user_id, chat_id, muted_until)

    # Методы работы с пользователями в чатах
    def approve_user(self, user_id: int, chat_id: int) -> Optional[ChatUser]:
        """Одобрить пользователя в чате."""
        return self.create_chat_user(user_id, chat_id)

    def remove_user_from_chat(self, user_id: int, chat_id: int) -> bool:
        """Удалить пользователя из чата."""
        return self.chat_user_repo.delete_chat_user(user_id, chat_id)

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Проверить, находится ли пользователь в чате."""
        return self.chat_user_repo.get_chat_user(user_id, chat_id) is not None

    def get_user_chats(self, user_id: int) -> List[Chat]:
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
