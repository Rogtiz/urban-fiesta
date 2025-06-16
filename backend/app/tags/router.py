from fastapi import APIRouter, Depends, HTTPException
from app.tags.schemas import STag
from app.tags.dao import TagsDAO
from app.users.auth import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)

@router.get("/")
async def get_tags(user: Users = Depends(get_current_user)) -> list[STag]:
    return await TagsDAO.get_all_tags()


@router.get("/user")
async def get_user_tags(user: Users = Depends(get_current_user)) -> list[STag]:
    return await TagsDAO.get_user_tags(user.id)


@router.get("/project/{project_id}")
async def get_project_tags(project_id: int, user: Users = Depends(get_current_user)) -> list[STag]:
    return await TagsDAO.get_project_tags(project_id)


@router.get("/{tag_id}")
async def get_tag_by_id(tag_id: int, user: Users = Depends(get_current_user)) -> STag:
    found_tag = await TagsDAO.find_by_id(tag_id)
    if not found_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    return found_tag


@router.post("/")
async def create_tag(tag: STag, user: Users = Depends(get_current_user)) -> STag:
    existed_tag = await TagsDAO.find_one_or_none(name=tag.name)
    if existed_tag:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    await TagsDAO.add(**tag.dict())
    return {"detail": "Tag created successfully"}


@router.post("/user/{tag_id}")
async def add_user_tag(tag_id: int, user: Users = Depends(get_current_user)) -> dict:
    user_tags = await TagsDAO.get_user_tags(user.id)
    if len(user_tags) >= 5:
        raise HTTPException(status_code=400, detail="User cannot have more than 5 tags")

    if any(tag.id == tag_id for tag in user_tags):
        raise HTTPException(status_code=400, detail="Tag is already attached to the user")
    await TagsDAO.add_user_tag(user.id, tag_id)
    return {"detail": "Tag added to user successfully"}


@router.post("/project/{project_id}/{tag_id}")
async def add_project_tag(project_id: int, tag_id: int, user: Users = Depends(get_current_user)) -> dict:
    project_tags = await TagsDAO.get_project_tags(project_id)
    if len(project_tags) >= 5:
        raise HTTPException(status_code=400, detail="Project cannot have more than 5 tags")
    
    if any(tag.id == tag_id for tag in project_tags):
        raise HTTPException(status_code=400, detail="Tag is already attached to the project")
    await TagsDAO.add_project_tag(project_id, tag_id)
    return {"detail": "Tag added to project successfully"}


@router.delete("/user/{tag_id}")
async def remove_user_tag(tag_id: int, user: Users = Depends(get_current_user)) -> dict:
    removed = await TagsDAO.remove_user_tag(user.id, tag_id)
    if not removed:
        raise HTTPException(status_code=404, detail="User tag not found")
    return {"detail": "Tag removed from user successfully"}


@router.delete("/project/{project_id}/{tag_id}")
async def remove_project_tag(project_id: int, tag_id: int, user: Users = Depends(get_current_user)) -> dict:
    removed = await TagsDAO.remove_project_tag(project_id, tag_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Project tag not found")
    return {"detail": "Tag removed from project successfully"}