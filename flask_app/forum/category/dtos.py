from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CategoryDTO:
    id: int
    name: str
    color: Optional[str]
    description: Optional[str]
    # topics: Optional[List]
