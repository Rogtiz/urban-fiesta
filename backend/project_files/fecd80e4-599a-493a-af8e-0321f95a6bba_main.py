from pydantic import BaseModel


class FileScheme(BaseModel):
    content: str
    new_file: str