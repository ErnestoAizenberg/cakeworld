from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class PostDTO:
    id: Optional[int] = None
    title: Optional[str] = None
    content: str = ""
    user_id: int = 0
    topic_id: int = 0
    post_id: Optional[int] = None
    created: datetime = field(default_factory=datetime.now)
    images: Optional[List[str]] = field(default_factory=list)
    views: Optional[List[int]] = field(default_factory=list)
