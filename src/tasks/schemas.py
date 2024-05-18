from typing import Optional
from pydantic import BaseModel
from datetime import date




class TaskCreate(BaseModel):
    """
Данный класс описывает схему данных для создания задачи.

Атрибуты:

    name: str - название задачи
    link: Optional[str] - ссылка на задачу
    lesson: str - название предмета
    type: Optional[str] - тип задачи
    deadline: Optional[datetime] - дедлайн задачи
    notion_id: Optional[int] - id задачи в Notion
    """

    name: str = 'Суть задачи'
    link: Optional[str] = None
    lesson: str = 'Название предмета'
    type: Optional[str] = None
    deadline: Optional[date] = None
    notion_id: Optional[int] = None


class TaskRead(TaskCreate):
    """
    Данный класс описывает схему данных для чтения задачи.
    
Атрибуты:

    name: str - название задачи
    link: Optional[str] - ссылка на задачу
    lesson: str - название предмета
    type: Optional[str] - тип задачи
    deadline: Optional[datetime] - дедлайн задачи
    notion_id: Optional[int] - id задачи в Notion

    """


    pass


class TaskUpdate(BaseModel):

    """
    Данный класс описывает схему данных для обновления задачи.

Атрибуты:

    id: int - id задачи
    name: str - название задачи
    link: Optional[str] - ссылка на задачу
    lesson: str - название предмета
    type: Optional[str] - тип задачи
    deadline: Optional[datetime] - дедлайн задачи
    notion_id: Optional[int] - id задачи в Notion
    """

    id: int
    name: str | None = None
    link: str | None = None
    lesson: str | None = None
    type: str | None = None
    deadline: date | None = None
    notion_id: int | None = None
