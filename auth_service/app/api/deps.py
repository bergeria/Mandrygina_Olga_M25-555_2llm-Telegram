"""
FastAPI dependencies Auth Service.

Содержит:
- dependency для БД
- фабрики репозиториев
- фабрики usecase
- зависимости проверки JWT
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.models import User
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UsersRepository:
    return UsersRepository(db)


def get_auth_uc(
    users_repo: Annotated[UsersRepository, Depends(get_users_repo)],
) -> AuthUseCase:
    return AuthUseCase(users_repo)


def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> int:
    try:
        payload = decode_token(token)
    except ValueError as exc:
        if str(exc) == "Token expired":
            raise TokenExpiredError() from exc
        raise InvalidTokenError() from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidTokenError()

    try:
        return int(user_id)
    except ValueError as exc:
        raise InvalidTokenError() from exc


async def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
) -> User:
    return await auth_uc.me(user_id)
