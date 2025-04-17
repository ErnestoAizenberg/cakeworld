from dataclasses import dataclass
from typing import Optional


@dataclass
class ChatDTO:
    id: Optional[int] = None
    title: str = "Untitled Chat"
    url_name: str = "untitled-chat"
    is_private: bool = False
    description: Optional[str] = None
    avatar_path: Optional[str] = None
