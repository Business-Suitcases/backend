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

    name: str
    link: Optional[str]
    lesson: str
    type: Optional[str]
    deadline: Optional[date]
    notion_id: Optional[int]


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


class TaskUpdate(TaskCreate):

    """
    Данный класс описывает схему данных для обновления задачи.

Атрибуты:

    name: str - название задачи
    link: Optional[str] - ссылка на задачу
    lesson: str - название предмета
    type: Optional[str] - тип задачи
    deadline: Optional[datetime] - дедлайн задачи
    notion_id: Optional[int] - id задачи в Notion
    """

    pass
