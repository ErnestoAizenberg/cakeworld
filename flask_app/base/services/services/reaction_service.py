# flask_app/services/reaction_service.py
from typing import Dict

from sqlalchemy import func

from ..models import Reaction
from .dtos.reaction_dto import ReactionDTO


class ReactionService:
    def __init__(self, db):
        self.db = db

    def get_reactions(self, message_id: int) -> Dict[str, int]:
        """Retrieve all reactions for a specific message."""
        reactions_count = (
            self.db.session.query(
                Reaction.emoji, func.count(Reaction.id).label("count")
            )
            .filter(Reaction.message_id == message_id)
            .group_by(Reaction.emoji)
            .all()
        )
        return {emoji: count for emoji, count in reactions_count}

    def react_to_message(self, user_id: int, message_id: int, emoji: str) -> None:
        """Add or update a reaction for a message."""
        existing_reaction = (
            self.db.session.query(Reaction)
            .filter_by(user_id=user_id, message_id=message_id)
            .first()
        )

        if existing_reaction:
            existing_reaction.emoji = emoji  # Update existing reaction
        else:
            new_reaction = Reaction(user_id=user_id, message_id=message_id, emoji=emoji)
            self.db.session.add(new_reaction)  # Add new reaction

        self.db.session.commit()
