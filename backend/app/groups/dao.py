from app.groups.models import Groups, ProjectGroups, UserGroups, Invitations
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users
from sqlalchemy import insert, select


class GroupsDAO(BaseDAO):
    model = Groups

    @classmethod
    async def get_user_groups(cls, user_id):
        async with async_session_maker() as session:
            query = select(Groups).outerjoin(UserGroups, Groups.id == UserGroups.group_id).where(
                (UserGroups.user_id == user_id) | (Groups.owner_id == user_id)
            ).distinct()
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def is_user_in_group(cls, user_id, group_id):
        async with async_session_maker() as session:
            query = select(UserGroups).where(UserGroups.user_id == user_id, UserGroups.group_id == group_id)
            result = await session.execute(query)
            return result.scalars().first() is not None
        
    @classmethod
    async def get_project_groups(cls, project_id):
        async with async_session_maker() as session:
            query = select(Groups).join(ProjectGroups, ProjectGroups.group_id == Groups.id).where(ProjectGroups.project_id == project_id)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def set_project_group(cls, project_id, group_id):
        async with async_session_maker() as session:
            query = insert(ProjectGroups).values(project_id=project_id, group_id=group_id)
            await session.execute(query)
            await session.commit()

    
    @classmethod
    async def set_user_group(cls, user_id, group_id):
        async with async_session_maker() as session:
            query = insert(UserGroups).values(user_id=user_id, group_id=group_id)
            await session.execute(query)
            await session.commit()

    
    @classmethod
    async def remove_user_group(cls, user_id, group_id):
        async with async_session_maker() as session:
            await session.execute(
                UserGroups.__table__.delete().where(UserGroups.user_id == user_id, UserGroups.group_id == group_id)
            )
            await session.commit()

    
    @classmethod
    async def delete_group(cls, group_id):
        async with async_session_maker() as session:
            # Delete relationships with users
            await session.execute(
                UserGroups.__table__.delete().where(UserGroups.group_id == group_id)
            )
            # Delete relationships with projects
            await session.execute(
                ProjectGroups.__table__.delete().where(ProjectGroups.group_id == group_id)
            )
            # Delete the group itself
            await session.execute(
                Groups.__table__.delete().where(Groups.id == group_id)
            )
            await session.commit()

    
    @classmethod
    async def get_group_members(cls, group_id):
        async with async_session_maker() as session:
            query = select(Users).join(UserGroups, Users.id == UserGroups.user_id).where(UserGroups.group_id == group_id)
            result = await session.execute(query)
            return result.scalars().all()
        


class InvitationsDAO(BaseDAO):
    model = Invitations

    @classmethod
    async def get_user_invitations(cls, user_id):
        async with async_session_maker() as session:
            query = select(Invitations).where(Invitations.receiver_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
        

    @classmethod
    async def update_status(cls, invitation_id, status):
        async with async_session_maker() as session:
            query = (
                Invitations.__table__.update()
                .where(Invitations.id == invitation_id)
                .values(status=status)
            )
            await session.execute(query)
            await session.commit()