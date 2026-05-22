#!/usr/bin/env bash

set -e

echo "Запуск инфраструктуры..."
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
else
  docker compose up -d
fi

echo "Ждем запуск контейнеров - 10 секунд..."
sleep 10

echo "Запуск  Auth Service..."
cd auth_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
AUTH_PID=$!
cd ..

echo "Запуск Bot Service API..."
cd bot_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BOT_API_PID=$!

echo "Запуск Celery Worker..."
uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info &
CELERY_PID=$!

echo "Запуск Telegram Bot..."
uv run python -m app.bot.run_bot &
TG_BOT_PID=$!
cd ..

echo ""
echo "Все процессы запущены."
echo "Auth Service: http://127.0.0.1:8000/docs"
echo "Bot Service:  http://127.0.0.1:8001/health"
echo ""
echo "Для останова нажмите Ctrl+C."

trap "echo 'Остановка ...'; kill $AUTH_PID $BOT_API_PID $CELERY_PID $TG_BOT_PID; exit" INT

wait

