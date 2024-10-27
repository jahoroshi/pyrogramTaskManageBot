import asyncio

import psycopg
from pyrogram.types import CallbackQuery

import bot_src.keyboards as kb
from bot_src.handlers.task.base_task_handler import BaseTaskHandler


class TaskStatusHandler(BaseTaskHandler):
    """Обработчик изменения статусов задач."""

    async def handle_status(self, _, callback_query: CallbackQuery) -> None:
        """Изменяет статус задачи на выполнена/невыполнена."""
        data = callback_query.data
        user_id = callback_query.from_user.id
        task_id = int(data.split("_")[1])
        query = "UPDATE tasks SET is_completed = NOT is_completed WHERE task_id = %s AND user_id = %s RETURNING is_completed"
        params = (task_id, user_id)
        try:
            response = await self.db.execute(query, params)
        except psycopg.Error:
            await callback_query.answer(
                "Ошибка при изменении статуса. Попробуйте еще раз."
            )
        else:
            if response and (r := response[0]):
                if r.get("is_completed"):
                    await callback_query.answer("Задача выполнена!")
                    await asyncio.sleep(1)
                    await callback_query.message.delete()
                else:
                    await callback_query.answer("Задача вновь активна!")
                    try:
                        task = await self._get_task(user_id, task_id)
                    except psycopg.Error:
                        await callback_query.message.reply(
                            "Произошла ошибка, попробуйте еще раз."
                        )
                        return

                    text = (
                        f"⏰ **{task.name}**\n" f"```Описание:\n{task.description}```"
                    )
                    await callback_query.edit_message_text(
                        text, reply_markup=kb.task_menu(task_id, False)
                    )
