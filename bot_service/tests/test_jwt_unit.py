"""
Модульные тесты проверки JWT Bot Service.

Проверяет:
- успешную валидацию JWT
- корректное извлечение payload
- обработку невалидного токена

Тесты выполняются без Redis и без Telegram.
"""

from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_and_validate_valid_token() -> None:
    payload = {
        "sub": "123",
        "role": "user",
        "iat": int(datetime.now(UTC).timestamp()),
        "exp": int((datetime.now(UTC) + timedelta(minutes=30)).timestamp()),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )

    decoded = decode_and_validate(token)

    assert decoded["sub"] == "123"
    assert decoded["role"] == "user"


def test_decode_and_validate_invalid_token() -> None:
    with pytest.raises(ValueError):
        decode_and_validate("invalid-token")
