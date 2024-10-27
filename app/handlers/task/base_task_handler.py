from typing import List

from app.database import Database
from app.models import Task
from app.states import FSMContext


class BaseTaskHandler:
    """Базовый класс для обработчиков задач."""

    def __init__(self, state: FSMContext, database: Database) -> None:
        self.state: FSMContext = state
        self.db: Database = database

    async def _get_tasks(self, user_id: int) -> List[Task]:
        """Получает список задач пользователя."""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s"
        tasks = await self.db.execute(query, (user_id,))
        return [Task(**el) for el in tasks]

    async def _get_task(self, user_id: int, task_id: int) -> Task:
        """Получает конкретную задачу пользователя."""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s AND task_id = %s"
        task = await self.db.get_one(query, (user_id, task_id))
        return Task(**task)
