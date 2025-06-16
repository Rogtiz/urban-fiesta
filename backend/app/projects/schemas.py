from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SProject(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    group_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class CreateProject(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True


class UpdateProject(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    group_id: Optional[int] = None

    class Config:
        from_attributes = True