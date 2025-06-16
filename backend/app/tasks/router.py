from fastapi import APIRouter, Depends, HTTPException
from app.tasks.schemas import STask, CreateTask, UpdateTask, SComment, CreateComment
from app.tasks.dao import TasksDAO, CommentsDAO
from app.users.auth import get_current_user
from app.users.models import Users
from app.projects.dao import ProjectsDAO
from app.groups.dao import GroupsDAO

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks and Comments"],
)

@router.get("/")
async def get_tasks(user: Users = Depends(get_current_user)) -> list[STask]:
    return await TasksDAO.get_user_tasks(user.id)


@router.get("/{task_id}")
async def get_task_by_id(task_id: int, user: Users = Depends(get_current_user)) -> STask:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id and found_task.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return found_task


@router.post("/")
async def create_task(task: CreateTask, user: Users = Depends(get_current_user)) -> STask:
    task.created_by = user.id
    current_project = await ProjectsDAO.find_by_id(task.project_id)
    if not current_project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not current_project.group_id:
        raise HTTPException(status_code=404, detail="Group not found")
    current_group = await GroupsDAO.find_by_id(current_project.group_id)
    if not current_group:
        raise HTTPException(status_code=404, detail="Group not found")
    if not await GroupsDAO.is_user_in_group(user.id, current_group.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this group")
    existed_task = await TasksDAO.find_one_or_none(title=task.title, created_by=user.id)
    if existed_task:
        raise HTTPException(status_code=400, detail="Task with this title already exists")
    created_task = await TasksDAO.add(**task.dict())
    return created_task


@router.put("/{task_id}")
async def update_task(task_id: int, task: UpdateTask, user: Users = Depends(get_current_user)) -> STask:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id and found_task.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    updated_task = await TasksDAO.update(task_id, **task.dict())
    return updated_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    await CommentsDAO.delete_task_comments(task_id)
    await TasksDAO.delete(task_id)
    return {"detail": "Task deleted successfully"}


@router.get("/{task_id}/comments")
async def get_task_comments(task_id: int, user: Users = Depends(get_current_user)) -> list[SComment]:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id and found_task.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return await CommentsDAO.get_task_comments(task_id)


@router.post("/{task_id}/comments")
async def create_comment(task_id: int, comment: CreateComment, user: Users = Depends(get_current_user)) -> SComment:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id and found_task.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    comment.user_id = user.id
    created_comment = await CommentsDAO.add(**comment.dict())
    return created_comment


@router.delete("/{task_id}/comments/{comment_id}")
async def delete_comment(task_id: int, comment_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_task = await TasksDAO.find_by_id(task_id)
    if not found_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if found_task.created_by != user.id and found_task.assigned_to != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    found_comment = await CommentsDAO.find_by_id(comment_id)
    if not found_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if found_comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    await CommentsDAO.delete(comment_id)
    return {"detail": "Comment deleted successfully"}