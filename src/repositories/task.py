import uuid
from typing import Sequence, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task, TaskStatus


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        """Создает новую задачу."""
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        """Получает задачу по ID."""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[Task]:
        """Получает список задач с пагинацией."""
        stmt = select(Task).limit(limit).offset(offset).order_by(Task.created_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(
        self, task_id: uuid.UUID, status: TaskStatus
    ) -> Optional[Task]:
        """Обновляет статус задачи."""
        stmt = (
            update(Task).where(Task.id == task_id).values(status=status).returning(Task)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()
