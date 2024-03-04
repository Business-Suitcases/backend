from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (Boolean, Column, String, Integer)
from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    tg_id = Column(Integer, autoincrement=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_superuser: bool = Column(Boolean, default=True, nullable=False)
