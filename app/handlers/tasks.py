from pyrogram import Client
from pyrogram.types import Message


class TasksHandler:
    """Обработчик задач."""

    def __init__(self):
        ...

    async def create_task(self, client: Client, message: Message):
        """Создание новой задачи"""