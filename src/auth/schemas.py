import uuid
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    tgid: Optional[int]
    username: str
    is_verified: bool = True


class UserCreate(schemas.BaseUserCreate):
    tgid: Optional[int]
    username: str
    is_verified: Optional[bool] = True

class UserUpdate(schemas.BaseUserUpdate):
    pass
