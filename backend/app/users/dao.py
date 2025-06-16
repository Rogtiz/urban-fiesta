from sqlalchemy import select
from app.dao.base import BaseDAO
from app.users.models import Users
from app.database import async_session_maker

class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def find_by_email(cls, email):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    
    @classmethod
    async def find_all_collaborators(cls, user_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(open_to_collab=True).filter(cls.model.id != user_id)
            result = await session.execute(query)
            return result.scalars().all()