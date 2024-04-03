import fastapi_users_db_sqlalchemy.generics
from sqlalchemy import Integer, String, ForeignKey, Column, Date
from src.auth.models import User
from src.database import Base
import fastapi_users_db_sqlalchemy


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255))
    lesson = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False, default="ДЗ")
    deadline = Column(Date)
    user_id = Column(fastapi_users_db_sqlalchemy.generics.GUID(), ForeignKey('user.id'))
