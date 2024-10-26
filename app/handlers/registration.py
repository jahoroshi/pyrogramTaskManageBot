import psycopg
from pyrogram.types import Message

import app.keyboards as kb
from app.database import Database
from app.models import User
from app.states import FSMContext
from app.states.states import Registration


class RegistrationHandler:
    """Обработчик регистрации пользователя."""

    def __init__(self, state: FSMContext, database: Database):
        self.state: FSMContext = state
        self.db: Database = database

    async def start(self, message: Message) -> None:
        """Обрабатывает команду start."""

        user_id: int = message.from_user.id
        user = await self.get_user(user_id)
        if user is None:
            await self.state.set_state(user_id, Registration.name)
            await message.reply("Введите имя!")
        else:
            await message.reply("С возвращением!", reply_markup=kb.main_menu())

    async def registration(self, message: Message) -> None:
        """Регистрация нового пользователя"""
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        a = (state == Registration.name)
        b = Registration.name
        print(a, 'a     b', b)
        if state and state == Registration.name:
            await self.state.set_state(user_id, Registration.username)
            await self.state.set_data(user_id, {"name": message.text})
            await message.reply("Введите имя пользователя:")
        elif state and state == Registration.username:
            state_data = await self.state.get_data(user_id)
            name: str = state_data.get("name")
            username: str = message.text
            try:
                query = "INSERT INTO users (user_id, name, username) VALUES (%s, %s, %s)"
                params = (user_id, name, username)
                await self.db.execute(query, params)
                await message.reply(
                    "Регистрация завершена успешно!", reply_markup=kb.main_menu()
                )
                await self.state.clear(user_id)
            except psycopg.errors.UniqueViolation:
                await message.reply(
                    "Пользователь с таким именем уже существует. Пожалуйста, введите другой логин:"
                )

    async def get_user(self, user_id: int) -> User | None:
        """Получает пользователя из базы."""
        query = "SELECT * FROM users WHERE user_id = %s"
        data = await self.db.get_one(query, (user_id,))
        if data:
            return User(**data)
        return
