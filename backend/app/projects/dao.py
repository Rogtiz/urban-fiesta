from app.groups.models import ProjectGroups, UserGroups
from app.projects.models import Projects
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select


class ProjectsDAO(BaseDAO):
    model = Projects

    @classmethod
    async def get_owned_projects(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.owner_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
        

    @classmethod
    async def get_member_projects(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .join(UserGroups, UserGroups.group_id == cls.model.group_id)
                .where(UserGroups.user_id == user_id)
            )
            result = await session.execute(query)
            return result.scalars().all()
        

    @classmethod
    async def get_all_user_projects(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .outerjoin(UserGroups, UserGroups.group_id == cls.model.group_id)
                .where((cls.model.owner_id == user_id) | (UserGroups.user_id == user_id))
                .distinct()  # Ensure no duplicates
            )
            result = await session.execute(query)
            return result.scalars().all()    