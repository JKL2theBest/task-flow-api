import logging.config
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.core.config import settings
from src.core.logging import LOGGING_CONFIG
from src.api.v1 import tasks

from fastapi.middleware.cors import CORSMiddleware

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="REST API для тестового задания (Task Management)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}
