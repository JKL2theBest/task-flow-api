# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
