"""
Точка входа Bot Service.

Создаёт экземпляр FastAPI
и предоставляет health-check endpoint.

Telegram-бот запускается отдельно.
"""

from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}
