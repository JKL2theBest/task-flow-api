import uuid
from typing import Sequence, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.task import Task, TaskStatus
from src.repositories.task import TaskRepository


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = TaskRepository(session)

    async def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """Бизнес-логика создания задачи."""
        new_task = Task(title=title, description=description)
        return await self.repository.create(new_task)

    async def get_task(self, task_id: uuid.UUID) -> Optional[Task]:
        return await self.repository.get_by_id(task_id)

    async def list_tasks(self, limit: int = 100, offset: int = 0) -> Sequence[Task]:
        return await self.repository.get_all(limit, offset)

    async def complete_task(self, task_id: uuid.UUID) -> Optional[Task]:
        """Бизнес-логика завершения задачи."""
        # TODO: нельзя завершить уже завершенную задачу
        return await self.repository.update_status(task_id, TaskStatus.COMPLETED)


# Dependency Injection
async def get_task_service(session: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(session)
