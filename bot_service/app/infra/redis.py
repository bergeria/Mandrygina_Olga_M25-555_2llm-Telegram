"""
Инфраструктурный модуль Redis.

Предоставляет singleton Redis-клиент
для хранения JWT и кэширования.
"""

from redis.asyncio import Redis

from app.core.config import settings


_redis: Redis | None = None


def get_redis() -> Redis:
    global _redis

    if _redis is None:
        _redis = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    return _redis

