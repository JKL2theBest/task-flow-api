import uuid
import pytest
from fastapi import status
from src.schemas.task import TaskResponse
from src.models.task import TaskStatus
from src.core.exceptions import TaskAlreadyCompletedError

pytestmark = pytest.mark.asyncio


async def test_create_task(client, mock_task_service):
    """Тест создания задачи"""
    task_id = uuid.uuid4()
    mock_task_service.create_task.return_value = TaskResponse(
        title="Test Task",
        description="Desc",
        id=task_id,
        status=TaskStatus.ACTIVE,
        created_at="2024-01-01T00:00:00",
        updated_at="2024-01-01T00:00:00",
    )

    response = await client.post(
        "/api/v1/tasks/", json={"title": "Test Task", "description": "Desc"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] == str(task_id)
    mock_task_service.create_task.assert_called_once_with(
        title="Test Task", description="Desc"
    )


async def test_get_task_not_found(client, mock_task_service):
    """Тест получения несуществующей задачи"""
    mock_task_service.get_task.return_value = None

    random_id = uuid.uuid4()
    response = await client.get(f"/api/v1/tasks/{random_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_complete_task_conflict(client, mock_task_service):
    """Тест попытки завершить уже завершенную задачу"""
    mock_task_service.complete_task.side_effect = TaskAlreadyCompletedError(
        "Already completed"
    )

    random_id = uuid.uuid4()
    response = await client.patch(f"/api/v1/tasks/{random_id}/complete")

    assert response.status_code == status.HTTP_409_CONFLICT
