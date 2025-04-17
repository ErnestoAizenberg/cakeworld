# flask_app/dto/reaction_dto.py
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReactionDTO:
    user_id: int
    message_id: int
    emoji: str
