import asyncio

import psycopg
from pyrogram.types import Message, CallbackQuery

import bot_src.keyboards as kb
from bot_src.handlers.task.base_task_handler import BaseTaskHandler
from bot_src.states.states import EditTask


class TaskEditingHandler(BaseTaskHandler):
    """Обработчик редактирования задач."""

    async def edit_task(self, _, callback_query: CallbackQuery):
        """Начинает процесс редактирования задачи."""
        data = callback_query.data
        user_id = callback_query.from_user.id
        task_id = int(data.split("_")[-1])
        if data.startswith("edit_task_name"):
            await self.state.set_state(user_id, EditTask.name)
            await self.state.set_data(user_id, {"task_id": task_id})
            await callback_query.message.reply("Введите новое название:")
        elif data.startswith("edit_task_disc"):
            await self.state.set_state(user_id, EditTask.description)
            await self.state.set_data(user_id, {"task_id": task_id})
            await callback_query.message.reply("Введите новое описание:")
        elif data.startswith("edit_task"):
            await callback_query.edit_message_reply_markup(
                reply_markup=kb.task_edit_name_discr(task_id)
            )

    async def edit_task_handler(self, _, message: Message):
        """Обрабатывает ввод пользователя при редактировании задачи."""
        text = message.text
        user_id = message.from_user.id
        data = await self.state.get_data(user_id)
        if data:
            task_id = data.get("task_id")
        else:
            await message.reply("У нас произошла ошибка. Попробуйте еще раз.")
            return
        cur_state = await self.state.get_state(user_id)
        field = "name" if cur_state == EditTask.name else "description"
        query = f"UPDATE tasks SET {field} = %s WHERE user_id = %s AND task_id = %s RETURNING task_id, name, description, is_completed"
        try:
            response = await self.db.execute(query, (text, user_id, task_id))
        except psycopg.Error:
            await message.reply("При изменении произошла ошибка. Повторите попытку.")
            await asyncio.sleep(1)
            await message.delete()
        else:
            if response and (res := response[0]):
                status = "✅" if res.get("is_completed") else "⏰"
                keyboard = kb.task_menu(res.get("task_id"), res.get("is_completed"))
                text = (
                    f"{status} **{res.get('name')}**\n"
                    f"```Описание:\n{res.get('description')}```"
                )
                await message.reply(
                    "🎉 __Задача успешно изменена__", reply_markup=kb.main_menu()
                )
                await self.state.clear(user_id)
                await asyncio.sleep(0.7)
                await message.reply(text, reply_markup=keyboard)

    async def back_to_taskmenu(self, _, callback_query: CallbackQuery):
        """Возвращает к главному меню задачи при редактировании."""
        data = callback_query.data
        user_id = callback_query.from_user.id
        task_id = int(data.split("_")[-1])
        try:
            task = await self._get_task(user_id, task_id)
        except psycopg.Error:
            await callback_query.message.reply("Произошла ошибка, попробуйте еще раз.")
            return

        await callback_query.edit_message_reply_markup(
            reply_markup=kb.task_menu(task_id, task.is_completed)
        )
