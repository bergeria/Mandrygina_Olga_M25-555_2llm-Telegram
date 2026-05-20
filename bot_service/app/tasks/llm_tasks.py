"""
Celery-задачи для обработки LLM-запросов.

Содержит:
- вызов OpenRouter
- обработку LLM-запросов
- отправку ответов пользователю в Telegram
"""

import asyncio

import httpx

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import OpenRouterClient


@celery_app.task(name="llm_request")
def llm_request(chat_id: int, prompt: str) -> str:
    return asyncio.run(run_llm_request(chat_id, prompt))


async def run_llm_request(chat_id: int, prompt: str) -> str:
    client = OpenRouterClient()

    try:
        response = await client.ask(prompt)
    except Exception as exc:
        response = f"Ошибка при обращении к LLM: {exc}"

    await send_telegram_message(chat_id, response)

    return response


async def send_telegram_message(chat_id: int, text: str) -> None:
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        await client.post(url, json=payload)
