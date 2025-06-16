from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.projects.router import router as projects_router
from app.users.router import router as users_router
from app.editor.router import router as editor_router
from app.files.router import router as files_router
from app.groups.router import router as groups_router
from app.tasks.router import router as tasks_router
from app.tags.router import router as tags_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # твой фронт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects_router)
app.include_router(users_router)
app.include_router(editor_router)
app.include_router(files_router)
app.include_router(groups_router)
app.include_router(tasks_router)
app.include_router(tags_router)

@app.get("/")
def read_root():
    return {"Info": "No info for now"}