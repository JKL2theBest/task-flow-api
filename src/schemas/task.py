import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.models.task import TaskStatus


# Базовая схема
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, description="Подробное описание")


# Схема для создания
class TaskCreate(TaskBase):
    pass


# Схема для ответа
class TaskResponse(TaskBase):
    id: uuid.UUID
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
