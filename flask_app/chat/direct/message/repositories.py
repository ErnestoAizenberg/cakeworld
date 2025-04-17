from typing import List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import MessageDTO
from .models import Message


class MessageRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Message, MessageDTO, db_session)

    def _to_dto(self, instance: Message) -> MessageDTO:
        return MessageDTO(
            id=instance.id,
            text=instance.text,
            user_id=instance.user_id,
            chat_id=instance.chat_id,
            created=instance.created,
            images=instance.images,
            views=instance.views,
        )

    def _from_dto(self, dto: MessageDTO) -> Message:
        return Message(
            id=dto.id,
            text=dto.text,
            user_id=dto.user_id,
            chat_id=dto.chat_id,
            created=dto.created,
            images=dto.images,
            views=dto.views,
        )

    def get_chat_messages(
        self, chat_id: int, offset: int, limit: int, user_id: int
    ) -> List[MessageDTO]:
        instances = (
            self.db_session.query(self.model)
            .filter_by(chat_id=chat_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._to_dto(instance) for instance in instances]

    def view_message(self, message_id: int, user_id: int) -> Optional[MessageDTO]:
        message = self.get(message_id)
        if message:
            message.views.append(user_id)
            self.save(message)
            return self._to_dto(message)
        return None

    def get_unread_count(self, chat_id: int, user_id: int) -> int:
        unread_msg_count = (
            self.db_session.query(Message)
            .filter(
                Message.chat_id == chat_id,
                Message.user_id != user_id,
                ~Message.views.contains(user_id),
            )
            .count()
        )
        return unread_msg_count
