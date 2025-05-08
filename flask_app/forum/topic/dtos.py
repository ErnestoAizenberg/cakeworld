from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TopicDTO:
    id: Optional[int] = None
    title: str = ""
    url_name: str = ""
    description: str = ""
    category_id: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
