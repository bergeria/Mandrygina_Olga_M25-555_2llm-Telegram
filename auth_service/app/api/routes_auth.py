"""
Маршруты аутентификации Auth Service.

Предоставляет endpoint-ы:
- регистрация пользователя
- логин пользователя
- получение профиля текущего пользователя
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user
from app.db.models import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
async def register(
    data: RegisterRequest,
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
) -> User:
    return await auth_uc.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_uc: Annotated[AuthUseCase, Depends(get_auth_uc)],
) -> TokenResponse:
    return await auth_uc.login(
        email=form.username,
        password=form.password,
    )


@router.get("/me", response_model=UserPublic)
async def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user
