import asyncio

import psycopg
from pyrogram.types import CallbackQuery

from app.handlers.task.base_task_handler import BaseTaskHandler


class TaskDeletionHandler(BaseTaskHandler):
    """Обработчик удаления задач."""

    async def delete_task(self, _, callback_query: CallbackQuery) -> None:
        """Удаляет задачу пользователя."""
        data = callback_query.data
        task_id = int(data.split("_")[1])
        user_id = callback_query.from_user.id
        query = "DELETE FROM tasks WHERE task_id = %s AND user_id = %s"
        try:
            await self.db.execute(query, (task_id, user_id))
        except psycopg.Error:
            await callback_query.answer("Ошибка при удалении задачи.")
        else:
            await callback_query.answer("Задача успешно удалена.")
            await asyncio.sleep(1.5)
            await callback_query.message.delete()
