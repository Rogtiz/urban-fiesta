from fastapi import APIRouter, Depends, HTTPException
from app.projects.schemas import SProject, CreateProject, UpdateProject
from app.projects.dao import ProjectsDAO
from app.groups.dao import GroupsDAO
from app.files.dao import FileDAO
from app.tasks.dao import TasksDAO
# from app.groups.schemas import SGroup
from app.users.auth import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)

@router.get("/")
async def get_projects(user: Users = Depends(get_current_user)) -> list[SProject]:
    
    return await ProjectsDAO.get_all_user_projects(user.id)


@router.get("/{project_id}")
async def get_project_by_id(project_id: int, user: Users = Depends(get_current_user)) -> SProject:
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        raise HTTPException(status_code=404, detail="Project not found")
    # if found_project.owner_id != user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to access this project")

    return found_project


@router.post("/")
async def create_project(project: CreateProject, user: Users = Depends(get_current_user)):
    project.owner_id = user.id
    existed_project = await ProjectsDAO.find_one_or_none(name=project.name, owner_id=user.id)
    if existed_project:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    await ProjectsDAO.add(**project.dict())
    return {"detail": "Project created successfully"}


@router.put("/{project_id}")
async def update_project(project_id: int, project: UpdateProject, user: Users = Depends(get_current_user)) -> SProject:
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if found_project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    updated_project = await ProjectsDAO.update(project_id, **project.dict())
    return updated_project


@router.delete("/{project_id}")
async def delete_project(project_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if found_project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    await ProjectsDAO.delete(project_id)
    return {"detail": "Project deleted successfully"}


@router.post("/{project_id}/groups/{group_id}")
async def add_group_to_project(project_id: int, group_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if found_project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if found_group.id in [group.id for group in await GroupsDAO.get_project_groups(project_id)]:
        raise HTTPException(status_code=400, detail="Group already added to this project")
    
    await GroupsDAO.set_project_group(project_id, group_id)

    return {"detail": "Group added to project successfully"}


@router.get("/{project_id}/files")
async def get_project_files(project_id: int, user: Users = Depends(get_current_user)):
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        return []
    
    # found_group = await GroupsDAO.get_project_groups(project_id)
    # if not found_group:
    #     raise HTTPException(status_code=404, detail="Group not found")
    # user_groups = await GroupsDAO.get_user_groups(user.id)
    # if not any(group.id in [g.id for g in found_group] for group in user_groups) or found_project.owner_id != user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to access this project")

    files = await FileDAO.get_project_files(project_id)
    return files


@router.get("/{project_id}/tasks")
async def get_project_tasks(project_id: int, user: Users = Depends(get_current_user)):
    found_project = await ProjectsDAO.find_by_id(project_id)
    if not found_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if found_project.owner_id == user.id:
        tasks = await TasksDAO.get_all_project_tasks(project_id)
    else:
        tasks = await TasksDAO.get_user_project_tasks(project_id, user.id)

    return tasks