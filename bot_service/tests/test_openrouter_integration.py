"""
Интеграционные тесты клиента OpenRouter.

Проверяет:
- корректное формирование HTTP-запроса
- обработку ответа OpenRouter API
- извлечение текста ответа LLM

Во время тестов используется respx
для мокирования HTTP-запросов.
"""

import pytest
import respx
from httpx import Response

from app.services.openrouter_client import OpenRouterClient


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_client_returns_answer() -> None:
    route = respx.post(
        "https://openrouter.ai/api/v1/chat/completions"
    ).mock(
        return_value=Response(
            status_code=200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": "Тестовый ответ LLM",
                        }
                    }
                ]
            },
        )
    )

    client = OpenRouterClient()

    result = await client.ask("Привет")

    assert result == "Тестовый ответ LLM"
    assert route.called
