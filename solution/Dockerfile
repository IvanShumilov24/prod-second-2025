FROM python:3.11-slim

WORKDIR /app
COPY . .


COPY pyproject.toml poetry.lock* ./
RUN pip install poetry
RUN pip install alembic
RUN pip install asyncpg
RUN pip install pydantic-settings
RUN poetry install --no-root
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]