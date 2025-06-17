import os
from fastapi import APIRouter, Body, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from app.files.schemas import FileVersionCreationSchema
from app.users.auth import get_current_user
from app.users.models import Users
from app.files.models import File as FileModel, FileVersion
from app.files.dao import FileDAO, FileVersionDAO
from uuid import uuid4
import aiofiles


UPLOAD_DIR = "project_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/files", tags=["Files"])

print("Imported")

@router.post("/upload/{project_id}")
async def upload_file(project_id: int, uploaded_file: UploadFile = File(...), user: Users = Depends(get_current_user)):
    filename = f"{uuid4()}_{uploaded_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # сохраняем на диск
    with open(file_path, "wb") as f:
        content = await uploaded_file.read()
        f.write(content)

    # записываем в базу
    new_file = FileModel(filename=uploaded_file.filename, path=file_path)
    await FileDAO.upload_file(new_file, project_id)

    return {"filename": uploaded_file.filename, "path": file_path}


@router.get("/{file_id}")
async def get_file_by_id(file_id: int, user: Users = Depends(get_current_user)):
    found_file = await FileDAO.find_by_id(file_id)
    if not found_file:
        raise HTTPException(status_code=404, detail="File not found in database")
    print(f"Found file: {found_file.filename} at {found_file.path}")
    files_project = await FileDAO.get_files_project(found_file.id)
    result = {
        "id": found_file.id,
        "filename": found_file.filename,
        "path": found_file.path,
        "project_id": files_project[0].project_id,
        "created_at": found_file.created_at,
    }
    return result


@router.get("/{file_id}/read", response_class=PlainTextResponse)
async def read_file_content(file_id: int, user: Users = Depends(get_current_user)):
    file = await FileDAO.find_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    version = await FileDAO.get_last_file_version(file_id)
    if version:
        file = version

    try:
        async with aiofiles.open(file.path, mode='r', encoding='utf-8') as f:
            content = await f.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found on disk")
    

@router.put("/{file_id}/save")
async def save_file(file_id: int, request: Request, user=Depends(get_current_user)):
    file = await FileDAO.find_by_id(file_id)
    if not file:
        raise HTTPException(404, "Файл не найден")
    
    version = await FileDAO.get_last_file_version(file_id)
    if version:
        file = version
    
    content_bytes = await request.body()

    async with aiofiles.open(file.path, "wb") as f:
        await f.write(content_bytes)

    return {"status": "saved"}



@router.get("/{file_id}/download")
async def download_file(file_id: int, user: Users = Depends(get_current_user)):
    file = await FileDAO.find_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(
        path=file.path,
        filename=file.filename,
        media_type="application/octet-stream"
    )


@router.get("/{version_id}/download_version")
async def download_version(version_id: int, user: Users = Depends(get_current_user)):
    file = await FileVersionDAO.find_by_id(version_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    filename = os.path.basename(file.path)
    return FileResponse(
        path=file.path,
        filename=filename,
        media_type="application/octet-stream"
    )


@router.post("/{file_id}/version/{description}")
async def create_file_version(
    file_id: int,
    request: Request,
    description: str = None,
    user: Users = Depends(get_current_user)
):
    file = await FileDAO.find_by_id(file_id)
    if not file:
        raise HTTPException(404, "Файл не найден")

    # Генерация уникального имени
    filename = f"{uuid4()}_{file.filename}"
    version_path = os.path.join("project_files/versions", filename)
    os.makedirs(os.path.dirname(version_path), exist_ok=True)

    content_bytes = await request.body()

    # Сохраняем файл на диск
    async with aiofiles.open(version_path, "wb") as f:
        await f.write(content_bytes)

    # Сохраняем метаинформацию в БД
    version = {
        "file_id": file_id,
        "path": version_path,
        "description": description,
        "user_id": user.id,
    }
    await FileVersionDAO.add(**version)

    return {"detail": "Версия сохранена"}


@router.get("/{file_id}/versions")
async def get_file_versions(file_id: int, user: Users = Depends(get_current_user)):
    file = await FileDAO.find_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    versions = await FileDAO.get_file_versions(file_id)
    return versions


@router.put("/version/{version_id}")
async def set_main_version(version_id: int):
    version = await FileVersionDAO.find_by_id(version_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Устанавливаем эту версию как основную
    await FileDAO.set_main_version(version_id)
    
    return {"detail": "Main version set successfully"}


@router.get("/test")
async def test_endpoint():
    return {"message": "It works!"}
