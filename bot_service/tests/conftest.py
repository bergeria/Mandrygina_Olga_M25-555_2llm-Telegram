"""
Общие pytest-фикстуры Bot Service.

Содержит:
- fake Redis через fakeredis
- fake Telegram message objects
- вспомогательные тестовые объекты

Используется mock-тестами Telegram handlers.
"""

from dataclasses import dataclass

import fakeredis.aioredis
import pytest_asyncio


@pytest_asyncio.fixture
async def fake_redis():
    redis = fakeredis.aioredis.FakeRedis(
        decode_responses=True,
    )
    yield redis
    await redis.aclose()

@dataclass
class FakeUser:
    id: int


@dataclass
class FakeChat:
    id: int


class FakeMessage:
    def __init__(self, text: str, user_id: int = 100, chat_id: int = 200):
        self.text = text
        self.from_user = FakeUser(id=user_id)
        self.chat = FakeChat(id=chat_id)
        self.answers: list[str] = []

    async def answer(self, text: str) -> None:
        self.answers.append(text)


@dataclass
class FakeCommand:
    args: str | None
