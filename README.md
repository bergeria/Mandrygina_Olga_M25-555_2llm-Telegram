еще не готово - тесты и демо.



# Двухсервисная система LLM-консультаций

Реализовано
1.  регистрация пользователя;
2.  логин пользователя;
3.  хранение пароля в виде bcrypt-хеша;
4.  выпуск JWT-токена;
5.  проверка JWT в Telegram Bot Service;
6.  хранение JWT в Redis по Telegram user_id;
7.  отправка LLM-запросов через Celery;
8.  RabbitMQ как брокер задач;
9.  Redis как backend и хранилище состояния;
10. OpenRouter как LLM-провайдер;
11. отправка ответа пользователю обратно в Telegram.
12. Тесты

Проект состоит из двух независимых сервисов:

- **Auth Service** — регистрация пользователей, логин, выпуск JWT-токенов.
- **Bot Service** — Telegram-бот, проверка JWT, отправка LLM-запросов через очередь.

Архитектура:

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


#Структура проекта

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
├── docker-compose.yml                     # Redis + RabbitMQ контейнеры
├── start.sh                               # Запуск проекта одним скриптом
├── stop.sh                                # Остановка проекта
├── README.md                              # Документация проекта и запуск
├── .env.example                           # Пример переменных окружения
└── .gitignore                             # Исключения Git


Пререквизиты

Python 3.11+
uv
Docker
Docker Compose
Telegram Bot Token - для этого Telegram бот уже должен быть создан
OpenRouter API Key

Установка системных зависимостей - Debian / Ubuntu

sudo apt update
sudo apt install -y curl git python3 python3-venv

Установка Docker из репозиториев дистрибутива:

sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker

Проверка:

docker --version
docker-compose --version

На некоторых системах вместо docker-compose используется новая команда:

docker compose version


Установка системных зависимостей в - Red Hat / Fedora

sudo dnf update -y
sudo dnf install -y curl git python3

Установка Docker:

sudo dnf install -y dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker

Проверка:

docker --version
docker compose version

Установка uv

curl -LsSf https://astral.sh/uv/install.sh | sh

После установки перезапустите терминал или выполните:

source ~/.bashrc

Проверка:

uv --version

Установка ruff

В корне проекта выполните uv add --dev ruff


Настройка Auth Service

В папке auth_service:

Создайте .env:

APP_NAME=auth-service
ENV=local

JWT_SECRET=change_me_super_secret
JWT_ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

SQLITE_PATH=./auth.db


Установите зависимости:
В папке auth_service выполните 

uv sync

Запуск Auth Service:
В папке auth_service выполните

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Swagger:

http://127.0.0.1:8000/docs

Health-check:

http://127.0.0.1:8000/health


Настройка Bot Service

В папке bot_service:

Создайте .env:

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

Важно: JWT_SECRET в auth_service/.env и bot_service/.env должен совпадать.

Установите зависимости:
В папке bot_service выполните

uv sync

Запуск Bot Service health API:

В отдельном терминале - из папки bot_service выполните 

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

Health-check:

http://127.0.0.1:8001/health



Запуск контейнера с Redis и RabbitMQ

Из корня проекта:

docker-compose up -d

Если используется новая версия Compose:

docker compose up -d

Проверка контейнеров:

docker ps

RabbitMQ UI:

http://localhost:15672

Логин и пароль:

guest / guest


Запуск Celery Worker

В отдельном терминале - из папки bot_service выполните 

uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info

В выводе должно быть:

[tasks]
 . llm_request

и:

celery ready


Запуск Telegram-бота

В отдельном терминале - из папки bot_service выполните 

uv run python -m app.bot.run_bot


Основные команды запуска - собрано в одно место файла.

Терминал 1 — инфраструктура
docker-compose up -d

или:

docker compose up -d

Терминал 2 — Auth Service
из папки auth_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Терминал 3 — Bot Service API
из папки bot_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

Терминал 4 — Celery Worker
из папки bot_service
uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info

Терминал 5 — Telegram Bot
из папки bot_service
uv run python -m app.bot.run_bot


Остановка проекта

Остановить сервисы в терминалах:

Ctrl+C

Остановить Docker-инфраструктуру:

docker-compose down

или:

docker compose down


для удобства есть скрипты запуска и остановки проекта

start.sh
stop.sh

Сначала нужно сделать скрипты исполняемым

chmod +x start.sh
chmod +x stop.sh

Запуск проекта

./start.sh

Остановка проекта

./stop.sh


Пользовательский сценарий


# После запуска проекта в любом браузере обратиться по адресу

# если с локального компьютера
http://localhost:8000/docs

# если другого компьютера
http://ip-address:8000/docs
# ip-address - ip адрес компьютера на котором запущен проект, в firewall должны быть соответствующие правила.

Зарегистрировать пользователя:
POST /auth/register
# Необходимо пройти процедуру регистрации пользователя - для этого нужны логин и пароль
# в качестве логина используйте email
# Выберите пункт - POST/auth/register и нажмите кнопку 'Try it out'
# в поле 'Request body' заполните логин и пароль, и потом нажмите 'Execute'


# Далее выполнить логин:
# Выберите пункт - POST /auth/login и нажмите кнопку 'Try it out'
# заполните логин и пароль, и потом нажмите 'Execute'
# Скопировать полученный JWT-токен.

#Отправить токен Telegram-боту:
/token <jwt-токен>

#После подтверждения можно начать общаться с ботом - отправьте свой вопрос:
Например - "Что такое Celery?"

#Бот отправит задачу в RabbitMQ, Celery Worker обработает её, вызовет OpenRouter и вернёт ответ в Telegram.


Запуск тестов

Auth Service

в каталоге auth_service выполнить

uv run pytest

Bot Service

в каталоге bot_service выполнить

uv run pytest


Screenshots

# Далее скриншоты - демонстрация работы Auth_service и Телеграмм бота.


# Регистрация пользователя
![Register](screenshots/register.png)

# Логин пользователя - логин и получение JWT
![Login](screenshots/login.png)

# Чат в Telegram-bot
![Chat](screenshots/chat.png)

# RabbitMQ - Overview
![RabbitMQ01](screenshots/RabbitMQ01.png)

# RabbitMQ - Queues
![RabbitMQ02](screenshots/RabbitMQ02.png)

# Тест Test_Auth_Service
![Test_Auth_Service](screenshots/test_auth_service.png)

# Тест Test_Bot_Service
![Bot_Auth_Service](screenshots/test_bot_service.png)










