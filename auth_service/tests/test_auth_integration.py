"""
Интеграционные тесты Auth Service.

Проверяет полный пользовательский сценарий:
- регистрацию пользователя
- логин пользователя
- доступ к /auth/me через JWT

Также содержит негативные тесты:
- повторная регистрация
- неверный пароль
- отсутствие JWT
- невалидный JWT
"""

from httpx import AsyncClient


async def test_register_login_and_me(client: AsyncClient) -> None:
    register_response = await client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "secret123",
        },
    )

    assert register_response.status_code == 200

    user_data = register_response.json()
    assert user_data["email"] == "student@example.com"
    assert user_data["role"] == "user"
    assert "password_hash" not in user_data

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "student@example.com",
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200

    token_data = login_response.json()
    assert token_data["token_type"] == "bearer"
    assert token_data["access_token"]

    me_response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token_data['access_token']}",
        },
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "student@example.com"


async def test_register_duplicate_email_returns_409(
    client: AsyncClient,
) -> None:
    payload = {
        "email": "duplicate@example.com",
        "password": "secret123",
    }

    first_response = await client.post("/auth/register", json=payload)
    second_response = await client.post("/auth/register", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409


async def test_login_with_wrong_password_returns_401(
    client: AsyncClient,
) -> None:
    await client.post(
        "/auth/register",
        json={
            "email": "wrong-password@example.com",
            "password": "secret123",
        },
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": "wrong-password@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


async def test_me_without_token_returns_401(client: AsyncClient) -> None:
    response = await client.get("/auth/me")

    assert response.status_code == 401


async def test_me_with_invalid_token_returns_401(client: AsyncClient) -> None:
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
