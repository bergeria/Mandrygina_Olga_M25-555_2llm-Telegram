"""
Пользовательские HTTP-исключения Auth Service.

Содержит набор специализированных исключений
для ошибок аутентификации и авторизации.
"""

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


class UserAlreadyExistsError(BaseHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует !"


class InvalidCredentialsError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный email или пароль !"


class InvalidTokenError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный token !"


class TokenExpiredError(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token просрочен !"


class UserNotFoundError(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Пользователь не найден !"


class PermissionDeniedError(BaseHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав !"
