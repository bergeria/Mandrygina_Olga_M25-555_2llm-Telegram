#!/usr/bin/env bash

set -e

echo "Starting infrastructure..."
if command -v docker-compose >/dev/null 2>&1; then
  docker-compose up -d
else
  docker compose up -d
fi

echo "Starting Auth Service..."
cd auth_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
AUTH_PID=$!
cd ..

echo "Starting Bot Service API..."
cd bot_service
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BOT_API_PID=$!

echo "Starting Celery Worker..."
uv run celery -A app.infra.celery_app:celery_app worker --loglevel=info &
CELERY_PID=$!

echo "Starting Telegram Bot..."
uv run python -m app.bot.run_bot &
TG_BOT_PID=$!
cd ..

echo ""
echo "All services started."
echo "Auth Service: http://127.0.0.1:8000/docs"
echo "Bot Service:  http://127.0.0.1:8001/health"
echo ""
echo "Press Ctrl+C to stop Python processes."

trap "echo 'Stopping...'; kill $AUTH_PID $BOT_API_PID $CELERY_PID $TG_BOT_PID; exit" INT

wait

