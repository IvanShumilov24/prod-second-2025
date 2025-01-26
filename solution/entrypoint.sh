#!/bin/sh
set -e

# Применяем миграции
./.venv/bin/python -m alembic upgrade head

# Запускаем uvicorn
exec ./.venv/bin/uvicorn "$@"
