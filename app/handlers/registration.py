from pyrogram import Client
from pyrogram.types import Message, User


class RegistrationHandler:
    """Обработчик регистрации пользователя."""

    def __init__(self):
        ...

    async def start(self, client: Client, message: Message) -> None:
        """Обрабатывает команду /start."""

        user_id: int = message.from_user.id
        user = await self.get_user(user_id)
        if user is None:
            # TODO: установка FSM
            await message.reply('Введите имя!')
        else:
            await message.reply('С возвращением!')

    async def registration(self, client: Client, message: Message) -> None:
        """Регистрация нового пользователя"""
        await message.reply('Регистрация пользователя')

    async def get_user(self, user_id: int) -> User | None:
        """Получает пользователя из базы данных."""
        return

