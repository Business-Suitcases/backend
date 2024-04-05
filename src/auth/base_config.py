import uuid
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend, CookieTransport, JWTStrategy)

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import SECRET_AUTH

half_year = 3600

cookie_transport = CookieTransport(cookie_name="hts", cookie_max_age=half_year)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=half_year)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()