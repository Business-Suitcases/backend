from typing import Optional
from fastapi import Depends, Request, Response
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)

from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    # Этот метод вызывается после регистрации пользователя.
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


    # Этот метод вызывается после входа пользователя.
    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        print(f"User {user.id} has logged in.")
        return await super().on_after_login(user, request, response)



    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


# Эта функция get_user_manager используется для получения экземпляра UserManager.
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
