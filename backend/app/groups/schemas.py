from typing import List
from pydantic import BaseModel

from app.users.schemas import UserSchema


class SGroup(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class SGroupCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class GroupResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    members: List[UserSchema] = []

    class Config:
        from_attributes = True


class InvitationCreate(BaseModel):
    sender_id: int
    receiver_id: int
    group_id: int
    message: str = None

    class Config:
        from_attributes = True