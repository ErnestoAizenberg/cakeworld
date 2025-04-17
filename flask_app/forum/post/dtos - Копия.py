from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class PostDTO:
    id: int
    title: Optional[str]
    content: str
    user_id: int
    topic_id: int
    post_id: Optional[int]
    created: datetime
    images: Optional[List[str]]
    views: Optional[List[int]]
