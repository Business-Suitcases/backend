from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.auth.schemas import UserCreate, UserRead
from src.config import REDIS_HOST, REDIS_PORT, SECRET_AUTH
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.manager import google_oauth_client


app = FastAPI(
    title="HomeTasks Application"
)

# Данный роутер используется для аутентификации пользователя.
app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth",
    tags=["Auth"],
)

# Данный роутер используется для аутентификации пользователя.
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# Данный роутер используется для обновления данных пользователя.
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, 
                                    auth_backend, SECRET_AUTH, 
                                    associate_by_email=True, 
                                    is_verified_by_default=True),
    prefix="/auth/google",
    tags=["Google OAuth2"],
)

# Данный роутер используется для ассоциации аккаунта Google с аккаунтом пользователя.
app.include_router(
    fastapi_users.get_oauth_associate_router(google_oauth_client, UserRead, SECRET_AUTH),
    prefix="/auth/associate/google",
    tags=["Google OAuth2"],
)

current_user = fastapi_users.current_user()


origins = [
    "http://localhost:3000"
]

# Строки ниже используются для разрешения запросов с других доменов (всех кроме localhost:3000 - то есть тех, что лежат в списке origins).
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                "Authorization"],
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
