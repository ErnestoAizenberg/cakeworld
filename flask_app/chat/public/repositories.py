from typing import List, Optional

from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import ChatDTO
from .models import Chat


class ChatRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Chat, ChatDTO, db_session)

    def _to_dto(self, instance: Chat) -> ChatDTO:
        return ChatDTO(
            id=instance.id,
            title=instance.title,
            url_name=instance.url_name,
            is_private=instance.is_private,
            description=instance.description,
            avatar_path=instance.avatar_path,
        )

    def _from_dto(self, dto: ChatDTO) -> Chat:
        return Chat(
            # id=dto.id,
            title=dto.title,
            url_name=dto.url_name,
            is_private=dto.is_private,
            description=dto.description,
            avatar_path=dto.avatar_path,
        )

    def get_chat_users(self, chat_id: int) -> List[int]:
        chat = self.db_session.query(self.model).get(chat_id)
        if chat:
            return [user.id for user in chat.users]
        return []

    def get_chat_by_url(self, url_name: str) -> Optional[ChatDTO]:
        instance = (
            self.db_session.query(self.model).filter_by(url_name=url_name).first()
        )
        if instance:
            return self._to_dto(instance)
        return None
