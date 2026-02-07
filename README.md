# Task Flow API

## Как запустить

### Вариант 1: Docker (Рекомендуется)

Самый быстрый способ запустить проект. Требуется только установленный Docker.

1.  Создайте файл `.env` из примера:
    ```bash
    cp .env.example .env
    ```
2.  Запустите проект одной командой:
    ```bash
    docker-compose up --build -d
    ```

Приложение будет доступно по адресу:
*   **Swagger UI (документация):** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Метрики Prometheus:** [http://localhost:8000/metrics](http://localhost:8000/metrics)

Миграции базы данных применяются автоматически при старте контейнера.

### Вариант 2: Локально (Poetry)

1.  Установите зависимости:
    ```bash
    poetry install
    ```
2.  Поднимите базу данных (пример через Docker):
    ```bash
    docker run --name pg-local -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=task_flow_db -p 5432:5432 -d postgres:17
    ```
3.  Примените миграции:
    ```bash
    poetry run alembic upgrade head
    ```
4.  Запустите сервер:
    ```bash
    poetry run uvicorn src.main:app --reload
    ```
