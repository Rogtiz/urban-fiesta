from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.tags.dao import TagsDAO
from app.users.dao import UsersDAO
from app.groups.dao import GroupsDAO
from app.projects.dao import ProjectsDAO

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"],
)


@router.get("/{telegram_id}/projects")
async def get_projects(telegram_id: int):
    user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    projects = await ProjectsDAO.get_all_user_projects(user.id)
    if not projects:
        return []
    
    return projects


@router.get("/{telegram_id}/groups")
async def get_groups(telegram_id: int):
    user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    groups = await GroupsDAO.get_user_groups(user.id)
    if not groups:
        return []
    
    return groups
