"""
Mock-тесты Telegram handlers Bot Service.

Проверяет:
- сохранение JWT в Redis
- обработку отсутствующего токена
- отправку задач в Celery
- корректный вызов llm_request.delay()

Во время тестов используются:
- fakeredis
- pytest-mock

Реальные Redis и RabbitMQ не используются.
"""

from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.bot import handlers
from app.core.config import settings


def create_test_token(user_id: int = 123, role: str = "user") -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(datetime.now(UTC).timestamp()),
        "exp": int((datetime.now(UTC) + timedelta(minutes=30)).timestamp()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


@pytest.mark.asyncio
async def test_token_command_saves_token(
    fake_redis,
    mocker,
) -> None:
    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    token = create_test_token()
    message = mocker.Mock()
    message.from_user.id = 100
    message.answer = mocker.AsyncMock()

    command = mocker.Mock()
    command.args = token

    await handlers.save_token(message, command)

    saved_token = await fake_redis.get("token:100")

    assert saved_token == token
    message.answer.assert_called_once()


@pytest.mark.asyncio
async def test_text_without_token_does_not_call_celery(
    fake_redis,
    mocker,
) -> None:
    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    celery_delay = mocker.patch(
        "app.bot.handlers.llm_request.delay",
    )

    message = mocker.Mock()
    message.text = "Что такое Celery?"
    message.from_user.id = 100
    message.chat.id = 200
    message.answer = mocker.AsyncMock()

    await handlers.handle_text(message)

    celery_delay.assert_not_called()
    message.answer.assert_called_once()

    answer_text = message.answer.call_args.args[0]
    assert "Сначала отправь JWT" in answer_text or "Доступ запрещён" in answer_text


@pytest.mark.asyncio
async def test_text_with_token_calls_celery(
    fake_redis,
    mocker,
) -> None:
    mocker.patch(
        "app.bot.handlers.get_redis",
        return_value=fake_redis,
    )

    celery_delay = mocker.patch(
        "app.bot.handlers.llm_request.delay",
    )
    celery_delay.return_value.id = "test-task-id"

    token = create_test_token()

    await fake_redis.set("token:100", token)

    message = mocker.Mock()
    message.text = "Что такое FastAPI?"
    message.from_user.id = 100
    message.chat.id = 200
    message.answer = mocker.AsyncMock()

    await handlers.handle_text(message)

    celery_delay.assert_called_once_with(
        200,
        "Что такое FastAPI?",
    )

    message.answer.assert_called_once()

    answer_text = message.answer.call_args.args[0]
    assert "Запрос принят" in answer_text
