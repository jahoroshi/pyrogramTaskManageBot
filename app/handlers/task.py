import asyncio
import time
from typing import List, Dict

import psycopg
from pyrogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.database import Database
from app.models import Task
from app.states import state
from app.states.fsm import FSMContext
from app.states.states import CreateTask, EditTask


class TaskHandler:
    """Интерфейс обработчика задач"""

    def __init__(self, state: FSMContext, database: Database) -> None:
        self.state: FSMContext = state
        self.db: Database = database

    async def create_task(self, _, message: Message) -> None:
        """Создание новой задачи"""
        user_id = message.from_user.id
        await self.state.set_state(user_id, CreateTask.name)
        await message.reply("Введите название задачи:")

    async def handle_task_creation(self, _, message: Message) -> None:
        """Обрабатывает создание задачи"""
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        if state and state == "CreateTask.name":
            await self.state.set_state(user_id, CreateTask.description)
            await self.state.set_data(user_id, {"name": message.text})
            await message.reply("Введите описание задачи:")
        elif state and state == "CreateTask.description":
            user_data: dict = await self.state.get_data(user_id)
            name: str = user_data.get("name")
            description: str = message.text
            query = "INSERT INTO tasks (user_id, name, description) VALUES (%s, %s, %s)"
            data = (user_id, name, description)
            try:
                await self.db.execute(query, data)
            except psycopg.Error:
                await message.reply('Произошла ошибка при добавлении задачи, попробуйте еще раз.')
            else:
                await message.reply(
                    "Задача успешно добавлена!", reply_markup=kb.main_menu()
                )

            await self.state.clear(user_id)

    async def list_tasks(self, _, message: Message) -> None:
        """Выводит все задачи пользователя"""
        user_id: int = message.from_user.id
        tasks: List[Task] = await self._get_tasks(user_id)
        if not tasks:
            await message.reply("Список задач пуст")
        else:
            for task in tasks:
                status: str = "✅" if task.is_completed else "⏰"
                keyboard = kb.task_menu(task.task_id, task.is_completed)
                text = (
                    f"{status} **{task.name}**"
                    f"```Описание:\n"
                    f"{task.description}\n"
                    f"```"
                )
                await message.reply(text, reply_markup=keyboard)

    async def handle_status(self, _, callback_query: CallbackQuery) -> None:
        """
        Изменение статуса задачи
        Изменение кнопки отметки задачи
        """
        data: str = callback_query.data
        user_id: int = callback_query.from_user.id
        task_id: int = int(data.split('_')[1])
        query = "UPDATE tasks SET is_completed = NOT is_completed WHERE task_id = %s AND user_id = %s RETURNING is_completed"
        params = (task_id, user_id)

        try:
            response = await self.db.execute(query, params)
        except psycopg.Error:
            await callback_query.answer('Ошибка при изменении статуса. Попробуйте еще раз.')
        else:

            # Проверяет ответ после обновления изменяет статус кнопки и тектс такски
            if response and (r := response[0]) and r.get('is_completed'):
                await callback_query.answer('Задача выполнена!')
                await asyncio.sleep(1.5)
                await callback_query.message.delete()
            elif response and (r := response[0]) and r.get('is_completed') is False:
                await callback_query.answer('Задача вновь активна!')
                task = await self._get_task(user_id, task_id)
                text = (
                    f"⏰ **{task.name}**"
                    f"```Описание:\n"
                    f"{task.description}\n"
                    f"```"
                )

                await callback_query.edit_message_text(text, reply_markup=kb.task_menu(task_id, False))


    async def delete_task(self, _, callback_query: CallbackQuery) -> None:
        """Удаляет выбранную задачу"""
        data: str = callback_query.data
        task_id: int = int(data.split('_')[1])
        user_id: int = callback_query.from_user.id
        query = "DELETE FROM tasks WHERE task_id = %s AND user_id = %s"
        try:
            await self.db.execute(query, (task_id, user_id))
        except psycopg.Error:
            await callback_query.answer('Ошибка при удалении задачи.')
        else:
            await callback_query.answer('Задача успешно удалена.')
            await asyncio.sleep(1.5)
            await callback_query.message.delete()


    async def _get_tasks(self, user_id: int) -> List[Task]:
        """Получает список задач"""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s"
        tasks = await self.db.execute(query, (user_id,))
        return [Task(**el) for el in tasks]


    async def _get_task(self, user_id: int, task_id) -> Task:
        """Получает одну задачу"""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s AND task_id = %s"
        task = await self.db.get_one(query, (user_id, task_id))
        return Task(**task)

    async def edit_task(self, _, callback_query: CallbackQuery):
        """
        Вызывается после нажатия inline-кнопки редактирования задачи
        Начинает процесс редактирования задачи
        В соответствии с нажатой inline-кнопкой ставится FMS редактирования
        :param _:
        :param callback_query:
        :return:
        """
        data = callback_query.data
        user_id = callback_query.from_user.id
        task_id = int(data.split('_')[-1])
        if data.startswith('edit_task_name'):
            await state.set_state(user_id, EditTask.name)
            await state.set_data(user_id, {'task_id': task_id})
            await callback_query.answer('Введите новое название:')
        elif data.startswith('edit_task_disc'):
            await state.set_state(user_id, EditTask.description)
            await state.set_data(user_id, {'task_id': task_id})
            await callback_query.answer('Введите новое описание:')
        elif data.startswith('edit_task'):
            await callback_query.edit_message_reply_markup(reply_markup=kb.task_edit_name_discr(task_id))

    async def edit_task_handler(self, client, message: Message):
        """
        Продолжается процесс редактирования задачи
        Вызывается если FSM находится в режиме редактирования задачи
        После успешного изменения выводится обновленная задача
        """
        text = message.text
        user_id = message.from_user.id
        data = await state.get_data(user_id)

        if data:
            task_id = data.get('task_id')
        else:
            await message.reply('У нас произошла ошибка. Попробуйте еще раз.')
            return

        cur_state = await state.get_state(user_id)

        # Выбирает какое поле редактировать в соотвестивии с установленных FSM
        field = 'name' if cur_state == EditTask.name else 'description'
        query = f"UPDATE tasks SET {field} = %s WHERE user_id = %s AND task_id = %s RETURNING task_id, name, description, is_completed"
        try:
            response = await self.db.execute(query, (text, user_id, task_id))
        except psycopg.Error:
            await message.reply(f'При изменении произошла ошибка. Повторите попытку.')
            await asyncio.sleep(1)
            await message.delete()
        else:
            if response and (res := response[0]) and isinstance(res, dict):
                status: str = "✅" if res.get('is_completed') else "⏰"
                keyboard = kb.task_menu(res.get('task_id'), res.get('is_completed'))
                text = (
                    "🎉 __Задача успешно изменена__\n"
                    f"{status} **{res.get('name')}**"
                    f"```Описание:\n"
                    f"{res.get('description')}\n"
                    f"```"
                )

                await message.reply(text, reply_markup=keyboard)



