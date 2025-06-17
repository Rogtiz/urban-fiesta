from datetime import datetime
from app.files.models import File, ProjectFile, FileVersion
from sqlalchemy import select, insert, update
from app.dao.base import BaseDAO
from app.database import async_session_maker


class FileDAO(BaseDAO):
    model = File

    @classmethod
    async def upload_file(cls, file, project_id):
        async with async_session_maker() as session:
            session.add(file)
            await session.flush()

            session.add(ProjectFile(project_id=project_id, file_id=file.id))
            await session.commit()
    
    @classmethod
    async def get_project_files(cls, project_id):
        async with async_session_maker() as session:
            stmt = select(File).join(ProjectFile).where(ProjectFile.project_id == project_id)
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @classmethod
    async def get_file_versions(cls, file_id):
        async with async_session_maker() as session:
            stmt = select(FileVersion).where(FileVersion.file_id == file_id).order_by(FileVersion.created_at.desc())
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @classmethod
    async def get_last_file_version(cls, file_id):
        async with async_session_maker() as session:
            stmt = select(FileVersion).where(FileVersion.file_id == file_id).order_by(FileVersion.created_at.desc()).limit(1)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
        
    @classmethod
    async def set_main_version(cls, version_id):
        async with async_session_maker() as session:
            await session.execute(update(FileVersion).where(FileVersion.id == version_id).values(created_at=datetime.utcnow()))
            await session.commit()

    @classmethod
    async def get_files_project(cls, file_id):
        async with async_session_maker() as session:
            stmt = select(ProjectFile).where(ProjectFile.file_id == file_id)
            result = await session.execute(stmt)
            return result.scalars().all()
    
class FileVersionDAO(BaseDAO):
    model = FileVersion
