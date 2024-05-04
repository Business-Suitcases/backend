from sqlalchemy import select
from src.tasks.models import Task
from src.tasks.schemas import TaskCreate, TaskUpdate
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from datetime import datetime
from datetime import timedelta
from fastapi import APIRouter
from src.tasks.models import Task
from src.tasks.utils import res_to_dict


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)




# Роутер для получения всех задач
@router.get('')
async def get(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных (`result`), и `None` в поле "details".

    """
    try:
        query = select(Task)

        res = await session.execute(query)
        result = res_to_dict(res)

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})














# Роутер для создания задачи
@router.post('')
async def create(task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
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

        return {
            "status_code": 201,
            "data": new_task,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
















# Роутер для обновления задачи
@router.put('')
async def update(task: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP PUT запроса для определенного маршрута. Она принимает следующие аргументы:

- `task` (тип `TaskUpdate`): представляет данные для обновления задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается экземпляр модели `Task` с аргументами, переданными в `task`.
2. Экземпляр модели добавляется в сессию `session`.
3. Сессия фиксируется с помощью `session.commit()`.
4. Функция возвращает словарь с данными, включающий статус код 200, обновленный объект задачи (`task`), и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        new_task = Task(**task.dict())
        session.add(new_task)
        await session.commit()

        return {
            "status_code": 200,
            "data": new_task,
            "details": None
        }
    except Exception as e:
        # Обработка исключений:
        if "duplicate key value violates unique constraint" in str(e):
            raise HTTPException(status_code=400, detail="Task with this notion_id already exists.")
        else:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
            print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})















# Роутер для удаления задачи
@router.delete('')
async def delete(task_id: int, session: AsyncSession = Depends(get_async_session)):
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

        return {
            "status_code": 200,
            "data": task,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})













# Роутер для получения задачи по идентификатору
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }

    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})













# Роутер для получения задач на текущий день
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})












# Роутер для получения задач на текущую неделю
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})












# Роутер для получения задач на текущий месяц
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})












# Роутер, который возвращает все задачи, отсортированных по параметру, заданным пользователем
@router.get('/sort')
async def sort_by(sort_by: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `sort_by` (тип `str`): представляет параметр, по которому необходимо отсортировать задачи.
- `session` (тип `AsyncSession`, по умолчанию `Depends(get_async_session)`): представляет асинхронную сессию для работы с базой данных.

Внутри функции происходит следующее:

1. Создается SQL-запрос с использованием библиотеки SQLAlchemy. Запрос выбирает все записи из таблицы `Task` и сортирует их по параметру, заданному в `sort_by`.
2. Запрос выполняется с помощью асинхронной сессии `session.execute(query)`.
3. Результат выполнения запроса сохраняется в переменную `result`.
4. Функция возвращает словарь с данными, включающий статус код 200, все полученные записи из базы данных, и `None` в поле "details".

Если в блоке `try` возникает исключение, то возвращается объект `HTTPException` с кодом состояния 500 и деталями ошибки, преобразованными в строку.
    """
    try:
        query = select(Task).order_by(Task.__dict__[sort_by])
        res = await session.execute(query)
        result = res_to_dict(res)

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})













# Роутер для получения первых n задач
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})











# Роутер для получения задач по категории
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    










# Роутер для получения задач по ссылке
@router.get('/by_link')
async def get_by_link(link: str, session: AsyncSession = Depends(get_async_session)):
    """
    Данная функция является обработчиком HTTP GET запроса для определенного маршрута. Она принимает следующие аргументы:

- `link` (тип `str`): представляет ссылку, по которой необходимо получить задачи.
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})















# Роутер для получения задач по типу
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
















# Роутер для получения задач по предмету
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    












# Роутер для получения задач по дедлайну
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})














# Роутер для получения задач по notion_id
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})
    













# Роутер для получения задач по срезу id от и до
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

        return {
            "status_code": 200,
            "data": result,
            "details": None
        }
    except Exception as e:
        # Тут пока для отладки выводится сама ошибка, но в продакшене так делать нельзя
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e), headers={"500": "Internal Server Error"})