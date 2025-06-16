from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class STask(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    project_id: int
    created_by: int
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None
    is_completed: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    created_by: int
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None
    is_completed: bool = False

    class Config:
        from_attributes = True


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    created_by: Optional[int] = None
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None

    class Config:
        from_attributes = True


class SComment(BaseModel):
    id: int
    text: str
    task_id: int
    user_id: int

    class Config:
        from_attributes = True


class CreateComment(BaseModel):
    text: str
    task_id: int
    user_id: int

    class Config:
        from_attributes = True