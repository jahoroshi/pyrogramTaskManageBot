from typing import List

from pyrogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.models import Task
from app.states.fsm import FSMContext
from app.states.states import CreateTask


class TaskHandler:
    """Обработчик задач."""

    def __init__(self, state: FSMContext) -> None:
        self.state: FSMContext = state

    async def create_task(self, message: Message) -> None:
        """Создание новой задачи"""
        user_id = message.from_user.id
        await self.state.set_state(user_id, CreateTask.name)
        await message.reply('Введите название задачи:')

    async def handle_task_creation(self, message: Message) -> None:
        """Обрабатывает создание задачи"""
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        if state and state == 'CreateTask.name':
            await self.state.set_state(user_id, CreateTask.description)
            await self.state.set_data(user_id, {'name': message.text})
            await message.reply('Введите описание задачи:')
        elif state and state == 'CreateTask.description':
            user_data: dict = await self.state.get_data(user_id)
            name: str = user_data.get('name')
            description: str = message.text
            # TODO: отправить в базу данные
            await self.state.clear(user_id)
            await message.reply('Задача успешно добавлена!', reply_markup=kb.main_menu())

    async def list_tasks(self, message: Message) -> None:
        """Выводит все задачи пользователя"""
        user_id: int = message.from_user.id
        tasks: List[Task] = await self.get_tasks(user_id)
        if not tasks:
            await message.reply('Список задач пуст')
        else:
            for task in tasks:
                status: str = 'OK' if task.is_completed else 'NO'
                keyboard = kb.task_menu(task.task_id, task.is_completed)
                await message.reply(f'{status} {task.name}', reply_markup=keyboard)

    async def callback_handler(self, query: CallbackQuery) -> None:
        """Обрабатывает нажатие кнопки"""
        ...

    async def get_tasks(self, user_id: int) -> List[Task]:
        """Получает список задач"""
        query = ...
        tasks = [
            {
                "task_id": 1,
                "user_id": 101,
                "title": "Buy groceries",
                "description": "Buy milk, bread, and eggs from the supermarket.",
                "completed": False
            },
            {
                "task_id": 2,
                "user_id": 102,
                "title": "Write report",
                "description": "Complete the financial report for Q3.",
                "completed": True
            }
        ]
        return [Task(*el) for el in tasks]
