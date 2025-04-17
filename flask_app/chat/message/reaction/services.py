# flask_app/services/reaction_service.py
from typing import Dict

from .dtos import ReactionDTO


class ReactionService:
    def __init__(self, reaction_repository: "ReactionRepository"):
        self.reaction_repository = reaction_repository

    def get_reactions(self, message_id: int) -> Dict[str, int]:
        """Retrieve all reactions for a specific message."""
        return self.reaction_repository.get_reactions_count_by_message(message_id)

    def react_to_message(self, user_id: int, message_id: int, emoji: str) -> None:
        """Add or update a reaction for a message."""
        reaction_dto = ReactionDTO(user_id=user_id, message_id=message_id, emoji=emoji)

        existing_reaction = self.reaction_repository.get_user_reaction(
            user_id, message_id
        )

        if existing_reaction:
            # Update existing reaction
            updated_reaction = ReactionDTO(
                user_id=user_id, message_id=message_id, emoji=emoji
            )
            self.reaction_repository.update(updated_reaction)
        else:
            # Add new reaction
            self.reaction_repository.save(reaction_dto)
