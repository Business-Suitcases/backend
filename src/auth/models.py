from datetime import datetime
from typing import ClassVar
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import (TIMESTAMP, Boolean, Column, ForeignKey, String, Integer)
from sqlalchemy.orm import relationship
from src.database import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):

    """
    Таблица аккаунтов OAuth

    id: int - идентификатор аккаунта
    account_email: str - почта аккаунта
    """

    __tablename__ = 'oauth_account'

    id = Column(Integer, primary_key=True)
    account_email = Column(String(length=320), ForeignKey('user.email'))


class User(SQLAlchemyBaseUserTable[int], Base):

    """
    Таблица пользователей
    
    id: int - идентификатор пользователя
    email: str - почта пользователя
    username: str - имя пользователя
    tg_id: int - идентификатор пользователя в телеграм
    hashed_password: str - хэшированный пароль
    is_superuser: bool - является ли пользователь суперпользователем
    registered_at: TIMESTAMP - время регистрации
    is_active: bool - активен ли пользователь
    is_verified: bool - верифицирован ли пользователь
    """

    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    email: str = Column(String, unique=True)
    username: str = Column(String, nullable=True, unique=True)
    tg_id: int = Column(Integer, autoincrement=False, nullable=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_superuser: bool = Column(Boolean, default=True, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.now())
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_verified: bool = Column(Boolean, default=True, nullable=False)
    oauth_accounts: ClassVar[OAuthAccount] = relationship("oauth_account", lazy="joined")
