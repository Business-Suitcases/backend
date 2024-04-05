import uuid
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    tgid: Optional[int]
    username: str


class UserCreate(schemas.BaseUserCreate):
    tgid: Optional[int]
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    pass
