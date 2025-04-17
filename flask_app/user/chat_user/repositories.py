from typing import List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository
from flask_app.chat.public.models import Chat
from flask_app.user.dtos import UserDTO
from flask_app.user.models import User

from .dtos import ChatUserDTO
from .models import ChatUser


class ChatUserRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(ChatUser, ChatUserDTO, db_session)

    def _to_dto(self, instance: ChatUser) -> ChatUserDTO:
        return ChatUserDTO(
            chat_id=instance.chat_id,
            user_id=instance.user_id,
            muted_until=instance.muted_until,
        )

    def _from_dto(self, dto: ChatUserDTO) -> ChatUser:
        return ChatUser(
            chat_id=dto.chat_id, user_id=dto.user_id, muted_until=dto.muted_until
        )

    def get_chat_user(self, user_id: int, chat_id: int) -> Optional[ChatUserDTO]:
        instance = (
            self.db_session.query(self.model)
            .filter_by(user_id=user_id, chat_id=chat_id)
            .first()
        )
        if instance:
            return self._to_dto(instance)
        return None

    def get_user_chats(self, user_id: int) -> List[int]:
        user = self.db_session.query(User).get(user_id)
        if user:
            return [chat.id for chat in user.chats]
        return []

    def _get_chat(self, chat_id) -> Chat:
        return self.db_session.query(Chat).get(chat_id)

    def get_chat_users(self, chat_id: int) -> List[UserDTO]:
        chat = self._get_chat(chat_id)
        return [self._to_dto(user) for user in chat.users]
