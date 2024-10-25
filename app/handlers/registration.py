from pyrogram.types import Message

import app.keyboards as kb
from app.models import User
from app.states import FSMContext
from app.states.states import Registration


class RegistrationHandler:
    """Обработчик регистрации пользователя."""

    def __init__(self, state: FSMContext):
        self.state: FSMContext = state

    async def start(self, message: Message) -> None:
        """Обрабатывает команду start."""

        user_id: int = message.from_user.id
        user = await self.get_user(user_id)
        user = 1
        if user is None:
            # TODO: установка FSM
            await message.reply('Введите имя!')
        else:
            await message.reply('С возвращением!', reply_markup=kb.main_menu())

    async def registration(self, message: Message) -> None:
        """Регистрация нового пользователя"""
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        if state and state == 'Registration.name':
            await self.state.set_state(user_id, Registration.username)
            await self.state.set_data(user_id, {'name': message.text})
            await message.reply('Введите имя пользователя:')
        elif state and state == 'Registration.username':
            state_data = await self.state.get_data(user_id)
            name: str = await state_data.get('name')
            username: str = message.text
            try:
                # TODO:отправляем в бд
                ...
                await message.reply('Регистрация завершена успешно!', reply_markup=kb.main_menu())
                await self.state.clear(user_id)
            except:
                await message.reply('Пользователь с таким именем уже существует. Пожалуйста, введите другой логин:')

    async def get_user(self, user_id: int) -> User | None:
        """Получает пользователя из базы."""
        query = ...
        data = ...
        if data:
            return User(*data)
        return
