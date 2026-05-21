#!/usr/bin/env bash

echo "Stopping Docker infrastructure..."

if command -v docker-compose >/dev/null 2>&1; then
  docker-compose down
else
  docker compose down
fi

echo "Stopping uvicorn, celery and bot processes..."

pkill -f "uvicorn app.main:app" || true
pkill -f "celery -A app.infra.celery_app:celery_app worker" || true
pkill -f "python -m app.bot.run_bot" || true

echo "All services stopped."

