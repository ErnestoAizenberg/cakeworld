# flask_app/repositories/reaction_repository.py
from typing import Dict, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from flask_app.base.repositories import BaseRepository

from .dtos import ReactionDTO
from .models import Reaction


class MessageReactionRepository(BaseRepository):
    def __init__(self, db_session: Session):
        super().__init__(Reaction, ReactionDTO, db_session)

    def _to_dto(self, instance: Reaction) -> ReactionDTO:
        """Convert Reaction model to ReactionDTO"""
        return ReactionDTO(
            user_id=instance.user_id,
            message_id=instance.message_id,
            emoji=instance.emoji,
        )

    def _from_dto(self, dto: ReactionDTO) -> Reaction:
        """Convert ReactionDTO to Reaction model"""
        return Reaction(user_id=dto.user_id, message_id=dto.message_id, emoji=dto.emoji)

    def get_reactions_count_by_message(self, message_id: int) -> Dict[str, int]:
        """Get reaction counts grouped by emoji for a specific message"""
        reactions_count = (
            self.db_session.query(
                Reaction.emoji, func.count(Reaction.id).label("count")
            )
            .filter(Reaction.message_id == message_id)
            .group_by(Reaction.emoji)
            .all()
        )
        return {emoji: count for emoji, count in reactions_count}

    def get_user_reaction(self, user_id: int, message_id: int) -> Optional[ReactionDTO]:
        """Get a user's reaction to a specific message"""
        reaction = (
            self.db_session.query(Reaction)
            .filter_by(user_id=user_id, message_id=message_id)
            .first()
        )
        return self._to_dto(reaction) if reaction else None
