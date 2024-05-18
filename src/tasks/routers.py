from sqlalchemy import select, update
from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskUpdate
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from datetime import datetime, date
from datetime import timedelta
from pydantic import HttpUrl
from fastapi import APIRouter
from src.tasks.models import Task
from src.tasks.utils import res_to_dict


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)




@router.get('')
async def task_get(sort_by: str = 'id', 
                in_ascending_order: bool = True, 
                start: int = 1, 
                end: int = 2_147_483_647, 
                session: AsyncSession = Depends(get_async_session)):

    """
    Данная функция является обработчиком HTTP GET. Она принимает следующие аргументы:

- `sort_by` (тип `str`, по умолчанию `'id'`): представляет название столбца, по которому необходимо отсортировать задачи.
- `in_ascending_order` (тип `bool`, по умолчанию `True`): представляет порядок сортировки задач.
- `start` (тип `int`, по умолчанию `1`): представляет начальное значение идентификатора задачи.
- `end` (тип `int`, по умолчанию `2_147_483_647`): представляет конечное значение идентификатора задачи.

    """
    

    query = select(Task).where((Task.id >= start) & (Task.id <= end))

    if in_ascending_order:
        query = query.order_by(Task.__dict__[sort_by].asc())
    else:
        query = query.order_by(Task.__dict__[sort_by].desc())


    try:
        res = await session.execute(query)
        result = res_to_dict(res)

    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks")

    return result





























@router.post('')
async def task_create(task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP POST запроса для определенного маршрута. Она принимает следующие аргументы:

- `task` (тип `TaskCreate`): представляет данные для создания новой задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается экземпляр модели `Task` с аргументами, переданными в `task`.
2. Экземпляр модели добавляется в сессию `session`.
3. Сессия фиксируется с помощью `session.commit()`.
4. Функция возвращает словарь с данными, включающий статус код "201", созданный объект задачи (`task`), и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        new_task = Task(**task.dict())
        session.add(new_task)
        await session.commit()

    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    return new_task

















@router.put('')
async def task_update(id: int,
    name: str | None = None,
    link: str | None = None,
    lesson: str | None = None,
    type: str | None = None,
    deadline: date | None = None,
    notion_id: int | None = None,
    session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP PUT запроса для определенного маршрута. Она принимает следующие аргументы:

- `id` (тип `int`): представляет идентификатор задачи, которую необходимо обновить.
- `name` (тип `str`, по умолчанию `None`): представляет новое название задачи.
- `link` (тип `str`, по умолчанию `None`): представляет новую ссылку задачи.
- `lesson` (тип `str`, по умолчанию `None`): представляет новый предмет задачи.
- `type` (тип `str`, по умолчанию `None`): представляет новый тип задачи.
- `deadline` (тип `date`, по умолчанию `None`): представляет новый дедлайн задачи.
- `notion_id` (тип `int`, по умолчанию `None`): представляет новый notion_id задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос обновляет запись в таблице `Task`, где значение столбца `id` равно `id`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Сессия фиксируется с помощью `session.commit()`.
4. Создается SQL-запрос для выбора обновленной задачи.
5. Результат выполнения запроса сохраняется в переменную `updated_task`.
6. Функция возвращает словарь с данными, включающий статус код 200, обновленный объект задачи (`updated_task`), и `None` в поле "details".
    """


    try:
        stmt = update(Task).where(Task.id == id)
        if name is not None:
            stmt = stmt.values(name=name)
        if link is not None:
            stmt = stmt.values(link=link)
        if lesson is not None:
            stmt = stmt.values(lesson=lesson)
        if type is not None:
            stmt = stmt.values(type=type)
        if deadline is not None:
            stmt = stmt.values(deadline=deadline)
        if notion_id is not None:
            stmt = stmt.values(notion_id=notion_id)

        await session.execute(stmt)
        await session.commit()

        stmt = select(Task).where(Task.id == id)
        result = await session.execute(stmt)
        updated_task = result.scalar()

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task
















@router.delete('')
async def task_delete(task_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP DELETE запроса для определенного маршрута. Она принимает следующие аргументы:

- `task_id` (тип `int`): представляет идентификатор задачи, которую необходимо удалить.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос удаляет запись из таблицы `Task`, где значение столбца `id` равно `task_id`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Сессия фиксируется с помощью `session.commit()`.
4. Функция возвращает словарь с данными, включающий статус код 200, удаленный объект задачи (`task`), и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.id == task_id)
        result = await session.execute(query)

        task = result.scalar()
        await session.delete(task)
        await session.commit()

    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task













@router.get('/by_column')
async def get_by_column(column: str, value: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `column` (тип `str`): представляет название столбца, по которому необходимо получить задачи.
- `value` (тип `str`): представляет значение, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `column` равно `value`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """

    value = value.strip()
    column = column.strip()

    if getattr(Task, column, None) is None:
        raise HTTPException(status_code=400, detail="There is no such column in the table")
    
    if column == 'id':
        value = int(value)

    try:
        query = select(Task).where(getattr(Task, column) == value)
        res = await session.execute(query)
        result = res.scalars().all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if not result:
        raise HTTPException(status_code=404, detail="There are no tasks with this value")
    
    return result












@router.get('/by_id')
async def get_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `task_id` (тип `int`): представляет идентификатор задачи, которую необходимо получить.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `id` равно `task_id`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, первую полученную запись из базы данных (`result.scalar()`), и `None` в поле "details".
    """
    try:
        query = select(Task).where(Task.id == id)
        result = await session.execute(query)
        result = result.scalar()


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    if result is None:
        raise HTTPException(status_code=404, detail="Id not found")
    
    return result




















@router.get('/by_name')
async def get_by_category(name: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `name` (тип `str`): представляет название, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `name` равно `name`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.name == name)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this name")
    
    return result











@router.get('/by_link')
async def get_by_link(link: HttpUrl, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `link` (тип `HttpUrl`): представляет ссылку, по которой необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `link` равно `link`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.link == link)
        res = await session.execute(query)
        result = res_to_dict(res)

    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this link")

    return result
















@router.get('/by_type')
async def get_by_type(type: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `type` (тип `str`): представляет тип, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `type` равно `type`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.type == type)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this type")

    return result

















@router.get('/by_lesson')
async def get_by_lesson(lesson: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `lesson` (тип `str`): представляет предмет, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `lesson` равно `lesson`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.lesson == lesson)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this lesson")
    
    return result













@router.get('/by_deadline')
async def get_by_deadline(deadline: datetime = datetime.now().date(), session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `deadline` (тип `datetime`): представляет дедлайн, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `deadline` равно `deadline`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.deadline == deadline)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this deadline")

    return result















@router.get('/by_notion_id')
async def get_by_notion_id(notion_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `notion_id` (тип `int`): представляет notion_id, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `notion_id` равно `notion_id`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.notion_id == notion_id)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this notion_id")
    
    return result














@router.get('/today')
async def get_today(session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `deadline` равно текущей дате.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных (`result.all()`), и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where(Task.deadline == datetime.now().date())

        res = await session.execute(query)
        result = res_to_dict(res)

    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks for today")
    
    return result













@router.get('/week')
async def get_week(session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `deadline` находится в текущей неделе.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where((Task.deadline >= datetime.now().date()) & (Task.deadline <= datetime.now().date() + timedelta(days=7)))
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks for this week")
    
    return result














@router.get('/month')
async def get_month(session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `deadline` находится в текущем месяце.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".



    """
    try:
        query = select(Task).where((Task.deadline >= datetime.now().date()) & (Task.deadline <= (datetime.now().date() + timedelta(days=30))))
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})

    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks for this month")
    
    return result















@router.get('/first_n')
async def get_first_n(n: int, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `n` (тип `int`): представляет количество задач, которые необходимо получить.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает первые `n` записей из таблицы `Task`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, первые `n` полученных записей из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).limit(n)
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks")
    
    return result
















@router.get('/by_id_range')
async def get_by_id_range(start: int, end: int, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `start` (тип `int`): представляет начало среза id, по которому необходимо получить задачи.
- `end` (тип `int`): представляет конец среза id, по которому необходимо получить задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task`, где значение столбца `id` находится в срезе от `start` до `end`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).where((Task.id >= start) & (Task.id <= end))
        res = await session.execute(query)
        result = res_to_dict(res)


    except Exception as e:

        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    
    if result is None:
        raise HTTPException(status_code=404, detail="There are no tasks with this id range")
    
    return result
