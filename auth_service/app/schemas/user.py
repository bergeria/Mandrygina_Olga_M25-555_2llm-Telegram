"""
Публичные схемы пользователя.

Содержит безопасное представление пользователя
без чувствительных данных, например password_hash.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

