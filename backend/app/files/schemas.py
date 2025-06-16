from pydantic import BaseModel, Field


class FileContent(BaseModel):
    content: str


class FileVersionCreationSchema(BaseModel):
    content: str
    description: str