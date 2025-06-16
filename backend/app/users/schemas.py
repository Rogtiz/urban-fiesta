from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Схема для групп
class GroupSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# Схема для проектов
class ProjectSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Схема для задач
class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None
    is_completed: bool

    class Config:
        from_attributes = True

# Схема пользователя (без пароля)
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    telegram_id: Optional[int] = None
    description: Optional[str] = None
    open_to_collab: bool = False
    disabled: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Финальная схема для полного ответа
class UserFullInfoSchema(BaseModel):
    user: UserSchema
    tags: List[TagSchema]
    groups: List[GroupSchema]
    owned_projects: List[ProjectSchema]
    member_projects: List[ProjectSchema]
    tasks: List[TaskSchema]



class UserCollaborators(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []



class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    open_to_collab: Optional[bool] = None

    class Config:
        from_attributes = True