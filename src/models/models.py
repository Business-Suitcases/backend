import fastapi_users_db_sqlalchemy.generics
from sqlalchemy import Integer, String, ForeignKey, Column, Date
from src.auth.models import User
from src.database import Base
import fastapi_users_db_sqlalchemy


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255))
    lesson = Column(String(255), nullable=False)
    type = Column(String(255), nullable=True, default="ДЗ")
    deadline = Column(Date)
    user_id = Column(fastapi_users_db_sqlalchemy.generics.GUID(), ForeignKey('user.id'))
    notion_id = Column(Integer)
