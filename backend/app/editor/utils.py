from sqlalchemy import select
from app.database import async_session_maker
from app.groups.models import Groups, UserGroups, ProjectGroups


async def is_user_allowed_to_edit(user_id: int, project_id: int) -> bool:
    async with async_session_maker() as session:
        result = await session.execute(
            select(Groups.id)
            .join(UserGroups, Groups.id == UserGroups.group_id)
            .join(ProjectGroups, Groups.id == ProjectGroups.group_id)
            .where(UserGroups.user_id == user_id, ProjectGroups.project_id == project_id)
        )
        return result.scalar() is not None