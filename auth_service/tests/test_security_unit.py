"""
Модульные тесты security-функций Auth Service.

Проверяет:
- хеширование паролей
- проверку паролей
- создание JWT
- декодирование JWT

Тесты выполняются без FastAPI и без базы данных.
"""

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password_and_verify_password() -> None:
    password = "secret123"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token() -> None:
    token = create_access_token(user_id=123, role="user")

    payload = decode_token(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload
