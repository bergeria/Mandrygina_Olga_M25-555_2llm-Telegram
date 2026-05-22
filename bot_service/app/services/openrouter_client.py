"""
Клиент OpenRouter API.

Реализует асинхронное взаимодействие
с OpenRouter chat completion API.
"""

import httpx

from app.core.config import settings


class OpenRouterError(Exception):
    pass


class OpenRouterClient:
    def __init__(self) -> None:
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model

    async def ask(self, prompt: str) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                )
        except httpx.HTTPError as exc:
            raise OpenRouterError(f"Запрос к OpenRouter завершился с ошибкой:"
                                  f"{exc}") from exc

        if response.status_code >= 400:
            raise OpenRouterError(
                f"OpenRouter вернул {response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise OpenRouterError("Неверный формат ответа от OpenRouter") from exc
