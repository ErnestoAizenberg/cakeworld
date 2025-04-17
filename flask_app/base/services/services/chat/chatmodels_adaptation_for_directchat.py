import uuid

from flask_app.services import ChatService, MessageService, UserService

from .models import Message, User


class DirectChat:
    def __init__(self, user1_id: int, user2_id: int):
        """Инициализация чата между двумя пользователями."""
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.chat_service = ChatService()
        self.message_service = MessageService()
        self.chat = self.get_or_create_chat()

    def get_or_create_chat(self):
        """Возвращает существующий директ чат между двумя пользователями или создаёт новый."""
        direct_chat = self.chat_service.get_chat_by_users(self.user1_id, self.user2_id)

        if not direct_chat:
            # Создаем новый директ чат
            direct_chat = self.chat_service.create_direct_chat(
                user1_id=self.user1_id,
                user2_id=self.user2_id,
                title=f"Chat between {self.user1_id} and {self.user2_id}",
            )

        return direct_chat

    def send_message(self, author_id: int, text: str):
        """Отправляет сообщение от одного из пользователей."""
        if author_id not in [self.user1_id, self.user2_id]:
            raise ValueError("User is not part of the direct chat")

        user = User.query.get(
            author_id
        )  # Этот запрос к базе данных остается здесь, чтобы получить имя пользователя
        message = self.message_service.create_message(
            text, user.username, author_id, self.chat.id
        )
        print("[DEBUG] Sent message:", message)

        return message

    def get_messages(self, limit=20, offset=0):
        """Получает все сообщения из личного чата с учетом пагинации."""
        return self.message_service.get_chat_messages(
            self.chat.id, offset, limit, self.user1_id
        )

    def mark_message_as_read(self, message_id: int, reader_id: int):
        """Отметить сообщение как прочитанное пользователем."""
        if reader_id not in [self.user1_id, self.user2_id]:
            raise ValueError("User is not part of the direct chat")

        self.message_service.mark_as_viewed(message_id, reader_id)

    def is_message_read(self, message_id: int, user_id: int) -> bool:
        """Проверяет, прочитано ли сообщение пользователем."""
        return self.message_service.is_message_read(message_id, user_id)


class DirectMessage:
    def __init__(self, message: Message):
        self.message = message

    def get_message_details(self):
        """Возвращает детали сообщения с информацией о прочтении."""
        return {
            "id": self.message.id,
            "text": self.message.text,
            "author": self.message.author,
            "created": self.message.created,
            "images": self.message.get_all_image_urls(),
            "is_read": {
                "user1": False,
                "user2": False,
            },
        }
