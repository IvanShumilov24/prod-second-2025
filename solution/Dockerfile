FROM python:3.11-slim

WORKDIR /app
COPY . .

ENV SERVER_ADDRESS ""
ENV SERVER_PORT ""
ENV POSTGRES_CONN ""
ENV POSTGRES_JDBC_URL ""
ENV POSTGRES_USERNAME ""
ENV POSTGRES_PASSWORD ""
ENV POSTGRES_HOST ""
ENV POSTGRES_PORT ""
ENV POSTGRES_DATABASE ""
ENV REDIS_HOST ""
ENV REDIS_PORT ""
ENV ANTIFRAUD_ADDRESS ""
ENV RANDOM_SECRET ""

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry
RUN pip install alembic
RUN pip install asyncpg
RUN pip install pydantic-settings
RUN poetry install --no-root

#RUN alembic upgrade head

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]