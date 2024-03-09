from typing import Optional

from fastapi_users import schemas
from sqlalchemy import true


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    tg_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = True

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    tg_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = True