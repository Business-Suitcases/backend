from sqlalchemy import Boolean, Integer, String, ForeignKey, Column, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    tgid = Column(Integer, autoincrement=False, unique=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)



class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255))
    lesson = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False, default="ДЗ")
    deadline = Column(Date)
    user_id = Column(Integer, ForeignKey(Users.id))



