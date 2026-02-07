import uuid
from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.task import Task, TaskStatus
from src.repositories.task import TaskRepository
from src.core.exceptions import TaskAlreadyCompletedError


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = TaskRepository(session)

    async def create_task(self, title: str, description: Optional[str] = None) -> Task:
        new_task = Task(title=title, description=description)
        return await self.repository.create(new_task)

    async def get_task(self, task_id: uuid.UUID) -> Optional[Task]:
        return await self.repository.get_by_id(task_id)

    async def list_tasks(self, limit: int = 100, offset: int = 0) -> Sequence[Task]:
        return await self.repository.get_all(limit, offset)

    async def complete_task(self, task_id: uuid.UUID) -> Optional[Task]:
        """Завершает задачу."""
        task = await self.repository.get_by_id(task_id)

        if not task:
            return None

        if task.status == TaskStatus.COMPLETED:
            raise TaskAlreadyCompletedError(f"Task {task_id} is already completed.")

        return await self.repository.update_status(task_id, TaskStatus.COMPLETED)


async def get_task_service(session: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(session)
