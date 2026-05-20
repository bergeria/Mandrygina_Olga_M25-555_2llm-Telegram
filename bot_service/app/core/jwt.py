"""
Модуль проверки JWT в Bot Service.

Bot Service не создаёт JWT-токены,
а только проверяет:
- подпись токена
- срок действия
- обязательные claims
"""

from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
    except ExpiredSignatureError as exc:
        raise ValueError("Token expired") from exc
    except JWTError as exc:
        raise ValueError("Invalid token") from exc

    if payload.get("sub") is None:
        raise ValueError("Invalid token: sub is missing")

    return payload
