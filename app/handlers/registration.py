from pyrogram import Client
from pyrogram.types import Message, User

from app.keyboards.menu import main_menu
from app.states import FSMContext


class RegistrationHandler:
    """Обработчик регистрации пользователя."""

    def __init__(self, state: FSMContext):
        self.state: FSMContext = state

    async def start(self, message: Message) -> None:
        """Обрабатывает команду /start."""

        user_id: int = message.from_user.id
        user = await self.get_user(user_id)
        user = 1
        if user is None:
            # TODO: установка FSM
            await message.reply('Введите имя!')
        else:
            await message.reply('С возвращением!', reply_markup=main_menu())

    async def registration(self, message: Message) -> None:
        """Регистрация нового пользователя"""
        await message.reply('Регистрация пользователя')

    async def get_user(self, user_id: int) -> User | None:
        """Получает пользователя из базы данных."""
        return

