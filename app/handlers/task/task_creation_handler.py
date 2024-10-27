import psycopg
from pyrogram.types import Message

import app.keyboards as kb
from app.handlers.task.base_task_handler import BaseTaskHandler
from app.states.states import CreateTask


class TaskCreationHandler(BaseTaskHandler):
    """Обработчик создания задач."""

    async def create_task(self, _, message: Message) -> None:
        """Начинает процесс создания новой задачи."""
        user_id = message.from_user.id
        await self.state.set_state(user_id, CreateTask.name)
        await message.reply("Введите название задачи:")

    async def handle_task_creation(self, _, message: Message) -> None:
        """Обрабатывает ввод пользователя при создании задачи."""
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        if state == "CreateTask.name":
            await self.state.set_state(user_id, CreateTask.description)
            await self.state.set_data(user_id, {"name": message.text})
            await message.reply("Введите описание задачи:")
        elif state == "CreateTask.description":
            user_data = await self.state.get_data(user_id)
            name = user_data.get("name")
            description = message.text
            query = "INSERT INTO tasks (user_id, name, description) VALUES (%s, %s, %s)"
            data = (user_id, name, description)
            try:
                await self.db.execute(query, data)
            except psycopg.Error:
                await message.reply(
                    "Произошла ошибка при добавлении задачи, попробуйте еще раз."
                )
            else:
                await message.reply(
                    "Задача успешно добавлена!", reply_markup=kb.main_menu()
                )
            await self.state.clear(user_id)
