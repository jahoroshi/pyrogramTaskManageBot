import asyncio
import time
from typing import List

import psycopg
from pyrogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.database import Database
from app.models import Task
from app.states.fsm import FSMContext
from app.states.states import CreateTask


class TaskHandler:
    """Обработчик задач."""

    def __init__(self, state: FSMContext, database: Database) -> None:
        self.state: FSMContext = state
        self.db: Database = database

    async def create_task(self, message: Message) -> None:
        """Создание новой задачи"""
        user_id = message.from_user.id
        await self.state.set_state(user_id, CreateTask.name)
        await message.reply("Введите название задачи:")

    async def handle_task_creation(self, message: Message) -> None:
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

    async def list_tasks(self, message: Message) -> None:
        """Выводит все задачи пользователя"""
        user_id: int = message.from_user.id
        tasks: List[Task] = await self.get_tasks(user_id)
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

    async def handle_status(self, callback_query: CallbackQuery) -> None:
        """Изменение статуса задачи"""
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
            if response and (r := response[0]) and r.get('is_completed'):
                await callback_query.answer('Задача выполнена!')
                await asyncio.sleep(1.5)
                await callback_query.message.delete()
            elif response and (r := response[0]) and r.get('is_completed') is False:
                await callback_query.answer('Задача вновь активна!')
                task = await self.get_task(user_id, task_id)
                text = (
                    f"⏰ **{task.name}**"
                    f"```Описание:\n"
                    f"{task.description}\n"
                    f"```"
                )

                await callback_query.edit_message_text(text, reply_markup=kb.task_menu(task_id, False))


    async def delete_task(self, callback_query: CallbackQuery) -> None:
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


    async def get_tasks(self, user_id: int) -> List[Task]:
        """Получает список задач"""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s"
        tasks = await self.db.execute(query, (user_id,))
        return [Task(**el) for el in tasks]


    async def get_task(self, user_id: int, task_id) -> Task:
        """Получает список задач"""
        query = "SELECT task_id, user_id, name, description, is_completed FROM tasks WHERE user_id = %s AND task_id = %s"
        task = await self.db.get_one(query, (user_id, task_id))
        return Task(**task)
