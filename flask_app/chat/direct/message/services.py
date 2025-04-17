from typing import List, Optional

from .models import Message
from .repositories import MessageRepository


class MessageService:
    def __init__(self, message_repo):
        self.message_repo = message_repo

    def create_message(self, text: str, user_id: int, chat_id: int) -> Message:
        """Создать сообщение."""
        new_message = Message(text=text, user_id=user_id, chat_id=chat_id)
        saved_message = self.message_repo.save(new_message)
        message_dto = self.map_message_data(saved_message)
        return message_dto

    def get_chat_messages(
        self, chat_id: int, offset: int, limit: int, user_id: int
    ) -> List[dict]:
        """Получить сообщения чата с отображением в нужном формате."""
        messages_feed = self.message_repo.get_chat_messages(
            chat_id, offset, limit, user_id
        )
        return self.map_messages_feed(messages_feed)

    def map_messages_feed(self, messages_feed: List[Message]) -> List[dict]:
        """Отобразить список сообщений в удобный формат."""
        return [self.map_message_data(message) for message in messages_feed]

    def map_reaction_data(self, reaction) -> dict:
        """Отобразить реакцию в удобный формат."""
        return {
            "id": reaction.id,
            "emoji": reaction.emoji,
            "user_id": reaction.user_id,
            "message_id": reaction.message_id,
        }

    def map_message_data(self, message: Message) -> dict:
        """Отобразить сообщение в удобный формат."""
        return {
            "id": message.id,
            "text": message.text,
            "user_id": message.user_id,
            "chat_id": message.chat_id,
            "created": str(message.created.time()),
            "images": message.images,
            "views": message.views if message.views else [],
            "reactions": [
                self.map_reaction_data(reaction) for reaction in message.reactions
            ],
        }

    def mark_as_viewed(self, message_id: int, user_id: int) -> Optional[Message]:
        """Отметить сообщение как прочитанное."""
        message = self.message_repo.view_message(message_id, user_id)
        if message:
            # Здесь можно добавить дополнительную логику, если необходимо
            pass
        return message

    def get_unread_count(self, chat_id: int, user_id: int) -> int:
        """Получить количество непрочитанных сообщений."""
        return self.message_repo.get_unread_count(chat_id, user_id)

    def is_message_read(self, message_id: int, user_id: int) -> bool:
        """Проверить, прочитано ли сообщение."""
        message = self.message_repo.get(message_id)
        return message.read_by.get(user_id, False) if message else False
