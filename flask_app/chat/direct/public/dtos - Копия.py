from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatDTO:
    id: int
    title: str
    url_name: str
    is_private: bool
    description: Optional[str]
    avatar_path: Optional[str]
