FROM python:3.11-slim-bookworm as builder

RUN pip install poetry

WORKDIR /solution
COPY README.md ./
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

FROM python:3.11-slim-bookworm as runner
WORKDIR /solution
COPY --from=builder /solution /solution
COPY alembic.ini .
WORKDIR .

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=4 --threads=1"

RUN pip install alembic
RUN pip install asyncpg
RUN pip install pydantic-settings
RUN pip install pydantic-extra-types
RUN pip install pycountry
RUN alembic upgrade head

CMD ["gunicorn", "solution.app.main:app", "--log-level", "info", "--log-file", "-"]
EXPOSE 8000