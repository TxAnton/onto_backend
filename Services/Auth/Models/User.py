from enum import Enum
from typing import List, Dict, Optional

from pydantic import BaseModel

class Action(Enum):
    Add=1
    Remove=2
    Clear=3

class Entity(BaseModel):
    ent_id: str


class UserIn(BaseModel):
    user_id: str
    data: Optional[Dict]
    links:List[str]

class ProjectIn(BaseModel):
    project_id: str
    data: Optional[Dict]
    links:List[str]