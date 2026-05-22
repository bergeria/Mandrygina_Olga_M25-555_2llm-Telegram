"""
Точка входа Auth Service.

Создаёт экземпляр FastAPI,
инициализирует таблицы базы данных
во время запуска приложения,
подключает роутеры и health-check endpoint.

Сервис отвечает только за:
- регистрацию пользователей
- аутентификацию
- выпуск JWT-токенов
- проверку JWT
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import settings
from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}
