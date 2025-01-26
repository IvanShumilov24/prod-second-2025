FROM python:3.11-slim

WORKDIR /app
COPY . .


COPY pyproject.toml poetry.lock* ./
RUN pip install poetry
RUN pip install alembic
RUN pip install asyncpg
RUN pip install pydantic-settings
RUN poetry install --no-root

ENTRYPOINT ["entrypoint.sh"]
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]