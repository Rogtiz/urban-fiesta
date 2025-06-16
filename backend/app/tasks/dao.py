from app.tasks.models import Tasks, Comments
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select

class TasksDAO(BaseDAO):
    model = Tasks

    @classmethod
    async def get_user_tasks(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).where((cls.model.created_by == user_id) | (cls.model.assigned_to == user_id))
            result = await session.execute(query)
            return result.scalars().all()
        
    
    @classmethod
    async def get_all_project_tasks(cls, project_id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.project_id == project_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    
    @classmethod
    async def get_user_project_tasks(cls, project_id, user_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .where(
                    (cls.model.created_by == user_id) | (cls.model.assigned_to == user_id),
                    cls.model.project_id == project_id
                )
            )
            result = await session.execute(query)
            return result.scalars().all()
    

class CommentsDAO(BaseDAO):
    model = Comments

    @classmethod
    async def get_task_comments(cls, task_id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.task_id == task_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def delete_task_comments(cls, task_id):
        async with async_session_maker() as session:
            await session.execute(
                cls.model.__table__.delete().where(cls.model.task_id == task_id)
            )
            await session.commit()