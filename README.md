# Двухсервисная система LLM-консультаций

Проект представляет собой распределённую систему LLM-консультаций, состоящую из двух независимых сервисов:

- **Auth Service** — регистрация пользователей, логин и выпуск JWT-токенов.
- **Bot Service** — Telegram-бот, проверка JWT и асинхронная обработка LLM-запросов.

Система построена по принципу разделения ответственности:

- Auth Service отвечает только за пользователей и JWT.
- Bot Service не хранит пользователей и не обращается к базе Auth Service.
- Bot Service доверяет только корректно подписанному JWT.

---

# Реализовано

- регистрация пользователя;
- логин пользователя;
- хранение пароля в виде bcrypt-хеша;
- выпуск JWT-токена;
- проверка JWT в Telegram Bot Service;
- хранение JWT в Redis по Telegram user_id;
- отправка LLM-запросов через Celery;
- RabbitMQ как брокер задач;
- Redis как backend и хранилище состояния;
- OpenRouter как LLM-провайдер;
- отправка ответа пользователю обратно в Telegram;
- unit / integration / mock тесты.

---

# Архитектура

```text
Telegram User
    ↓
Telegram Bot / aiogram
    ↓
JWT validation + Redis
    ↓
Celery task
    ↓
RabbitMQ
    ↓
Celery Worker
    ↓
OpenRouter API
    ↓
Telegram User
```

---

# Используемые технологии

- FastAPI
- aiogram
- SQLAlchemy Async
- SQLite
- Redis
- RabbitMQ
- Celery
- OpenRouter
- httpx
- pytest
- pytest-asyncio
- fakeredis
- pytest-mock
- respx
- Docker
- uv
- Ruff

---

# Структура проекта

```text
.
├── auth_service/
│   ├── app/                               # Исходный код Auth Service
│   │   ├── __init__.py
│   │   │
│   │   ├── api/                           # FastAPI API-слой
│   │   │   ├── __init__.py
│   │   │   ├── deps.py                    # FastAPI dependencies
│   │   │   ├── router.py                  # Агрегация роутеров
│   │   │   └── routes_auth.py             # Endpoint-ы аутентификации
│   │   │
│   │   ├── core/                          # Базовые компоненты приложения
│   │   │   ├── __init__.py
│   │   │   ├── config.py                  # Конфигурация приложения
│   │   │   ├── exceptions.py              # Пользовательские HTTP-исключения
│   │   │   └── security.py                # JWT и хеширование паролей
│   │   │
│   │   ├── db/                            # Работа с базой данных
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # Базовый класс SQLAlchemy
│   │   │   ├── models.py                  # ORM-модели БД
│   │   │   └── session.py                 # Async engine и sessionmaker
│   │   │
│   │   ├── repositories/                  # Репозитории доступа к данным
│   │   │   ├── __init__.py
│   │   │   └── users.py                   # CRUD-операции для пользователей
│   │   │
│   │   ├── schemas/                       # Pydantic-схемы
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                    # Схемы JWT и регистрации
│   │   │   └── user.py                    # Публичные схемы пользователя
│   │   │
│   │   ├── usecases/                      # Бизнес-логика приложения
│   │   │   ├── __init__.py
│   │   │   └── auth.py                    # Логика регистрации и логина
│   │   │
│   │   └── main.py                        # Точка входа FastAPI Auth Service
│   │
│   ├── tests/                             # Тесты Auth Service
│   │   ├── __init__.py
│   │   ├── conftest.py                    # Общие pytest-фикстуры
│   │   ├── test_security_unit.py          # Unit-тесты security-функций
│   │   └── test_auth_integration.py       # Интеграционные HTTP-тесты Auth API
│   │
│   ├── .env                               # Переменные окружения Auth Service
│   ├── auth.db                            # SQLite база данных
│   ├── pyproject.toml                     # Зависимости auth_service через uv
│   ├── pytest.ini                         # Настройки pytest
│   └── uv.lock                            # Lock-файл зависимостей uv
│
├── bot_service/
│   ├── app/                               # Исходный код Bot Service
│   │   ├── __init__.py
│   │   │
│   │   ├── bot/                           # Telegram Bot на aiogram
│   │   │   ├── __init__.py
│   │   │   ├── dispatcher.py              # Bot и Dispatcher aiogram
│   │   │   ├── handlers.py                # Telegram handlers
│   │   │   └── run_bot.py                 # Запуск Telegram-бота
│   │   │
│   │   ├── core/                          # Базовые компоненты Bot Service
│   │   │   ├── __init__.py
│   │   │   ├── config.py                  # Конфигурация приложения
│   │   │   └── jwt.py                     # Проверка JWT-токенов
│   │   │
│   │   ├── infra/                         # Инфраструктурный слой
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py              # Конфигурация Celery
│   │   │   └── redis.py                   # Redis-клиент
│   │   │
│   │   ├── services/                      # Внешние сервисы и API-клиенты
│   │   │   ├── __init__.py
│   │   │   └── openrouter_client.py       # Клиент OpenRouter API
│   │   │
│   │   ├── tasks/                         # Celery background tasks
│   │   │   ├── __init__.py
│   │   │   └── llm_tasks.py               # LLM-задачи Celery worker
│   │   │
│   │   └── main.py                        # FastAPI health API Bot Service
│   │
│   ├── tests/                             # Тесты Bot Service
│   │   ├── __init__.py
│   │   ├── conftest.py                    # Общие pytest-фикстуры
│   │   ├── test_jwt_unit.py               # Unit-тесты проверки JWT
│   │   ├── test_handlers_mock.py          # Mock-тесты Telegram handlers
│   │   └── test_openrouter_integration.py # Интеграционные тесты OpenRouter-клиента
│   │
│   ├── .env                               # Переменные окружения Bot Service
│   ├── pyproject.toml                     # Зависимости bot_service через uv
│   ├── pytest.ini                         # Настройки pytest
│   └── uv.lock                            # Lock-файл зависимостей uv
│
├── screenshots/
│   ├── register.png
│   ├── login.png
│   ├── chat.png
│   ├── rabbitmq_overview.png
│   ├── rabbitmq_queues.png
│   ├── test_auth_service.png
│   └── test_bot_service.png
│
├── docker-compose.yml                     # Redis + RabbitMQ контейнеры
├── start.sh                               # Запуск проекта одним скриптом
├── stop.sh                                # Остановка проекта
├── README.md                              # Документация проекта и запуск
├── .env.example                           # Пример переменных окружения
└── .gitignore                             # Исключения Git

```

---

# Требования

- Python 3.11+
- uv
- Docker
- Docker Compose
- Telegram Bot Token
- OpenRouter API Key

---

# Установка системных зависимостей

## Debian / Ubuntu

```bash
sudo apt update
sudo apt install -y curl git python3 python3-venv
```

### Установка Docker

```bash
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

### Проверка

```bash
docker --version
docker-compose --version
```

На некоторых системах вместо `docker-compose` используется:

```bash
docker compose version
```

---

## Fedora / Red Hat

```bash
sudo dnf update -y
sudo dnf install -y curl git python3
```

### Установка Docker

```bash
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo

sudo dnf install -y \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin
```

```bash
sudo systemctl enable --now docker
```

### Проверка

```bash
docker --version
docker compose version
```

---

# Установка uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

После установки:

```bash
source ~/.bashrc
```

Проверка:

```bash
uv --version
```

---

# Настройка Auth Service

Перейти в каталог:

```bash
cd auth_service
```

Создать `.env`:

```env
APP_NAME=auth-service
ENV=local

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./auth.db
```

Установить зависимости:

```bash
uv sync
```

---

# Запуск Auth Service

Из каталога `auth_service`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health-check:

```text
http://127.0.0.1:8000/health
```

---

# Настройка Bot Service

Перейти в каталог:

```bash
cd bot_service
```

Создать `.env`:

```env
APP_NAME=bot-service
ENV=local

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256

REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=stepfun/step-3.5-flash:free
OPENROUTER_SITE_URL=https://example.com
OPENROUTER_APP_NAME=bot-service
```

> Важно:
> JWT_SECRET в `auth_service/.env` и `bot_service/.env` должен совпадать.

Установить зависимости:

```bash
uv sync
```

---

# Запуск Bot Service API

Из каталога `bot_service`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Health-check:

```text
http://127.0.0.1:8001/health
```

---

# Запуск Redis и RabbitMQ

Из корня проекта:

```bash
docker compose up -d
```

или:

```bash
docker-compose up -d
```

Проверка контейнеров:

```bash
docker ps
```

RabbitMQ UI:

```text
http://localhost:15672
```

Логин и пароль:

```text
guest / guest
```

---

# Запуск Celery Worker

Из каталога `bot_service`:

```bash
uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info
```

В выводе должно быть:

```text
[tasks]
 . llm_request
```

и:

```text
celery ready
```

---

# Запуск Telegram-бота

Из каталога `bot_service`:

```bash
uv run python -m app.bot.run_bot
```

---

# Основные команды запуска

## Терминал 1 — инфраструктура

```bash
docker compose up -d
```

---

## Терминал 2 — Auth Service

Из каталога `auth_service`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Терминал 3 — Bot Service API

Из каталога `bot_service`:

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

---

## Терминал 4 — Celery Worker

Из каталога `bot_service`:

```bash
uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info
```

---

## Терминал 5 — Telegram Bot

Из каталога `bot_service`:

```bash
uv run python -m app.bot.run_bot
```

---

# Автоматический запуск проекта

Для удобства используются скрипты:

```text
start.sh
stop.sh
```

Сделать их исполняемыми:

```bash
chmod +x start.sh
chmod +x stop.sh
```

Запуск проекта:

```bash
./start.sh
```

Остановка проекта:

```bash
./stop.sh
```

---

# Пользовательский сценарий

1. Открыть Swagger:

```text
http://localhost:8000/docs
```

2. Зарегистрировать пользователя через:

```text
POST /auth/register
```

3. Выполнить логин через кнопку `Authorize`.

4. Скопировать JWT-токен.

5. Отправить токен Telegram-боту:

```text
/token <jwt-token>
```

6. Отправить вопрос боту.

Например:

```text
Что такое Celery?
```

7. Bot Service:
- валидирует JWT;
- публикует задачу в RabbitMQ;
- Celery Worker вызывает OpenRouter;
- ответ возвращается пользователю в Telegram.

---

# Виды тестирования

Проект содержит:

- unit tests;
- integration tests;
- mock tests.

Используются:

- pytest;
- pytest-asyncio;
- fakeredis;
- pytest-mock;
- respx.

---

# Запуск тестов

## Auth Service

Из каталога `auth_service`:

```bash
uv run pytest
```

---

## Bot Service

Из каталога `bot_service`:

```bash
uv run pytest
```

---

# Скриншоты работы проекта

## Регистрация пользователя

![Register](screenshots/register.png)

---

## Логин пользователя и получение JWT

![Login](screenshots/login.png)

---

## Работа Telegram-бота

![Chat](screenshots/chat.png)

---

## RabbitMQ Overview

![RabbitMQ Overview](screenshots/rabbitmq_overview.png)

---

## RabbitMQ Queues

![RabbitMQ Queues](screenshots/rabbitmq_queues.png)

---

## Тестирование Auth Service

![Auth Tests](screenshots/test_auth_service.png)

---

## Тестирование Bot Service

![Bot Tests](screenshots/test_bot_service.png)

---

# Результат

Проект реализует двухсервисную архитектуру LLM-консультаций:

- Auth Service отвечает за пользователей и JWT;
- Bot Service отвечает за Telegram и LLM;
- RabbitMQ используется как broker Celery;
- Redis используется как backend и хранилище JWT;
- OpenRouter используется как LLM provider.

Система поддерживает:

- JWT-аутентификацию;
- асинхронную обработку задач;
- Telegram-интерфейс;
- unit / integration / mock тестирование.
