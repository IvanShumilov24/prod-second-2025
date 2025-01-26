FROM python:3.11-slim

WORKDIR /app
COPY . .

ENV SERVER_ADDRESS "0.0.0.0:8080"
ENV SERVER_PORT "8080"
ENV POSTGRES_CONN ""
ENV POSTGRES_JDBC_URL ""
ENV POSTGRES_USERNAME ""
ENV POSTGRES_PASSWORD ""
ENV POSTGRES_HOST "localhost"
ENV POSTGRES_PORT "5432"
ENV POSTGRES_DATABASE ""
ENV REDIS_HOST "localhost"
ENV REDIS_PORT "6379"
ENV ANTIFRAUD_ADDRESS "localhost:9090"
ENV RANDOM_SECRET ""

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry
RUN pip install alembic
RUN pip install asyncpg
RUN pip install pydantic-settings
RUN poetry install --no-root

RUN alembic upgrade head

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]