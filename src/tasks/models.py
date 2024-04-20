from sqlalchemy import Integer, String, Column, Date
from src.database import Base


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    link = Column(String(255))
    lesson = Column(String(255), nullable=False)
    type = Column(String(255), nullable=True, default="ДЗ")
    deadline = Column(Date)
    notion_id = Column(Integer)
