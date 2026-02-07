import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.task import TaskCreate, TaskResponse
from src.services.task import TaskService, get_task_service

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    """Создать новую задачу."""
    return await service.create_task(
        title=task_in.title, description=task_in.description
    )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    service: TaskService = Depends(get_task_service),
):
    """Получить список задач."""
    return await service.list_tasks(limit=limit, offset=skip)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
):
    """Получить задачу по ID."""
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: uuid.UUID,
    service: TaskService = Depends(get_task_service),
):
    """Завершить задачу."""
    task = await service.complete_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task
