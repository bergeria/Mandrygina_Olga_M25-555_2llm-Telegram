Mandrygina_Olga_M25-555_2llm-Telegram/
├── auth_service/
│   ├── app/
│   ├── pyproject.toml
│   └── uv.lock
│
├── bot_service/
│   ├── app/
│   ├── pyproject.toml
│   └── uv.lock
│
├── docker-compose.yml
├── README.md
└── .gitignore

Запустить auth_service

cd ./auth_service
uv sync

Нужно заполнить ./auth_service/.env

Далее в терминал выполнить

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


Нужно заполнить ./bot_service/.env

TELEGRAM_BOT_TOKEN=test
OPENROUTER_API_KEY=test

Запускаем bot

cd ./bot_service
uv sync

Далее в другом окне терминала выполнить 

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001


Создаем docker-compose.yml

services:

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"

  redis:
    image: redis:7
    ports:
      - "6379:6379"
     
     
Из корня проекта:

docker compose up -d

Проверка RabbitMQ

в браузере открыть 

http://localhost:15672

Логин : guest

Пароль : guest

если docker не установлен - В Debian :

sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker

Далее создаем контейнер

sudo docker-compose up -d

Чтобы не писать sudo - Добавьте себя в группу docker:

sudo usermod -aG docker $USER

После этого - выйди из системы и зайди снова.


Можно запущенные посмотреть контейнеры:

docker ps

В списке запущенных контейнеров должны быть 

Redis
RabbitMQ

Проверяем RabbitMQ UI

Откройте в браузере - в Debian:

http://localhost:15672

Логин : guest

Пароль  guest

Проверка Redis ????

Запуск worker

В Debian-host нужно обращаться через:

localhost

REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672//

Из папки:

./bot_service/

выполни:

uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info

На этом этапе можно сделать предварительную проверку работоспособности связки модулей
???
Celery worker принимает задачи
RabbitMQ доставляет их
Redis хранит результат
OpenRouter отвечает


в каталоге ./bot_service/ выполнить

uv run python

потом ввести команды

from app.tasks.llm_tasks import llm_request
task = llm_request.delay("Привет! Здесь Ваш вопрос ???")
task.get(timeout=120)

если все .env файлы заполнены корректными данными, то Вы должны получить ответ от OpenRouter



