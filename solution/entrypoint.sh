#!/bin/sh
set -e

./.venv/bin/poetry run alembic upgrade head

exec "./.venv/bin/uvicorn" "$@"
