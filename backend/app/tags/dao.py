from sqlalchemy import select
from app.tags.models import Tags, ProjectTags, UserTags
from app.dao.base import BaseDAO
from app.database import async_session_maker

class TagsDAO(BaseDAO):
    model = Tags

    @classmethod
    async def get_all_tags(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_user_tags(cls, user_id):
        async with async_session_maker() as session:
            query = select(Tags).join(UserTags, UserTags.tag_id == Tags.id).where(UserTags.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def get_project_tags(cls, project_id):
        async with async_session_maker() as session:
            query = select(Tags).join(ProjectTags, ProjectTags.tag_id == Tags.id).where(ProjectTags.project_id == project_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add_user_tag(cls, user_id, tag_id):
        async with async_session_maker() as session:
            new_user_tag = UserTags(user_id=user_id, tag_id=tag_id)
            session.add(new_user_tag)
            await session.commit()
            return new_user_tag
        
    @classmethod
    async def add_project_tag(cls, project_id, tag_id):
        async with async_session_maker() as session:
            new_project_tag = ProjectTags(project_id=project_id, tag_id=tag_id)
            session.add(new_project_tag)
            await session.commit()
            return new_project_tag
        
    @classmethod
    async def remove_user_tag(cls, user_id, tag_id):
        async with async_session_maker() as session:
            query = select(UserTags).where(UserTags.user_id == user_id, UserTags.tag_id == tag_id)
            result = await session.execute(query)
            user_tag = result.scalars().first()
            if user_tag:
                await session.delete(user_tag)
                await session.commit()
                return True
            return False
        
    @classmethod
    async def remove_project_tag(cls, project_id, tag_id):
        async with async_session_maker() as session:
            query = select(ProjectTags).where(ProjectTags.project_id == project_id, ProjectTags.tag_id == tag_id)
            result = await session.execute(query)
            project_tag = result.scalars().first()
            if project_tag:
                await session.delete(project_tag)
                await session.commit()
                return True
            return False