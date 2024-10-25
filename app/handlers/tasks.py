from typing import List

from pyrogram.types import Message, CallbackQuery

from app.models import Task
from app.states.fsm import FSMContext
from app.states.states import CreateTask


class TasksHandler:
    """Обработчик задач."""

    def __init__(self, state: FSMContext) -> None:
        self.state: FSMContext = state
        ...

    async def create_task(self, _, message: Message) -> None:
        """Создание новой задачи"""
        user_id = message.from_user.id
        self.state.set_state(user_id, CreateTask.name)
        await message.reply('Введите название задачи:')

    async def handle_task_creation(self, _, message: Message) -> None:
        """Обрабатывает создание задачи"""
        user_id = message.from_user.id
        state = self.state.get_state(user_id)
        if state and state == 'CreateTask.name':
            self.state.set_state(user_id, CreateTask.description)
            self.state.set_data(user_id, {'name': message.text})
            await message.reply('Введите описание задачи:')
        elif state and state == 'CreateTask.description':
            user_data: dict = self.state.get_data(user_id)
            name: str = user_data.get('name')
            description: str = message.text
            # TODO: отправить в базу данные
            self.state.clear(user_id)
            await message.reply('Задача успешно добавлена!')

    async def list_tasks(self, _, message: Message) -> None:
        """Выводит все задачи пользователя"""
        user_id: int = message.from_user.id
        tasks: List[Task] = await self.get_tasks(user_id)
        if not tasks:
            await message.reply('Список задач пуст')
        else:
            for task in tasks:
                status: str = 'OK' if task.is_completed else 'NO'
                keyboard = ...
                await message.reply(f'{status} {task.name}')

    async def callback_handler(self, _, query: CallbackQuery) -> None:
        """Обрабатывает нажатие кнопки"""
        ...

    async def get_tasks(self, user_id: int) -> List[Task]:
        """Получает список задач"""
        query = ...
        tasks = {}
        return [Task(*el) for el in tasks]