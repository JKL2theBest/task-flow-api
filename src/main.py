from fastapi import FastAPI
from src.core.config import settings
from src.api.v1 import tasks

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="REST API для тестового задания (Task Management)",
    version="1.0.0",
)

app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.PROJECT_NAME}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
