import psycopg
from pyrogram.types import Message

import bot_src.keyboards as kb
from bot_src.handlers.task.base_task_handler import BaseTaskHandler


class TaskListingHandler(BaseTaskHandler):
    """Обработчик отображения списка задач."""

    async def list_tasks(self, _, message: Message) -> None:
        """Выводит список всех задач пользователя."""
        user_id = message.from_user.id
        try:
            tasks = await self._get_tasks(user_id)
        except psycopg.Error:
            await message.reply("Произошла ошибка, попробуйте еще раз.")
            return

        if not tasks:
            await message.reply("Список задач пуст")
        else:
            for task in tasks:
                status = "✅" if task.is_completed else "⏰"
                keyboard = kb.task_menu(task.task_id, task.is_completed)
                text = (
                    f"{status} **{task.name}**\n" f"```Описание:\n{task.description}```"
                )
                await message.reply(text, reply_markup=keyboard)
