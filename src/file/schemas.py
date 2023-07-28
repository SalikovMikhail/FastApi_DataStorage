from datetime import datetime

from pydantic import BaseModel, Json

from src.auth.schemas import UserRead

class FileCreate(BaseModel):
    id: int
    name: str
    download_at: datetime
    data: Json
    user_id: int
    path: str

class FileGet(BaseModel):
    id: int
    name: str
    download_at: datetime | str
    user: UserRead | int
    path: str
