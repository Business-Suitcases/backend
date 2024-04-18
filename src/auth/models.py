from typing import List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import (Column, String, Integer)
from sqlalchemy.orm import relationship, Mapped
from src.database import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):

    """
    Таблица аккаунтов OAuth

    id: uuid - идентификатор аккаунта
    account_email: str - почта аккаунта
    """

    pass


class User(SQLAlchemyBaseUserTableUUID, Base):

    """
    Таблица пользователей
    
    id: uuid - идентификатор пользователя
    email: str - почта пользователя
    username: str - имя пользователя
    tg_id: int - идентификатор пользователя в телеграм
    hashed_password: str - хэшированный пароль
    is_superuser: bool - является ли пользователь суперпользователем
    registered_at: TIMESTAMP - время регистрации
    is_active: bool - активен ли пользователь
    is_verified: bool - верифицирован ли пользователь
    """

    tgid = Column(Integer)
    username = Column(String(255), nullable=True)

    oauth_accounts: Mapped[List[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")