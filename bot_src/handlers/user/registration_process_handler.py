import psycopg
from pyrogram.types import Message

import bot_src.keyboards as kb
from bot_src.handlers.user.base_user_handler import BaseUserHandler
from bot_src.states.states import Registration


class RegistrationProcessHandler(BaseUserHandler):
    """Обрабатывает ввод данных для регистрации пользователя."""

    async def registration(self, _, message: Message) -> None:
        user_id = message.from_user.id
        state = await self.state.get_state(user_id)
        if state == Registration.name:
            await self.state.set_state(user_id, Registration.username)
            await self.state.set_data(user_id, {"name": message.text})
            await message.reply("Введите имя пользователя:")
        elif state == Registration.username:
            state_data = await self.state.get_data(user_id)
            name: str = state_data.get("name")
            username: str = message.text
            try:
                query = (
                    "INSERT INTO users (user_id, name, username) VALUES (%s, %s, %s)"
                )
                params = (user_id, name, username)
                try:
                    await self.db.execute(query, params)
                except psycopg.Error:
                    await message.reply("Произошла ошибка, попробуйте еще раз.")
                    return

                await message.reply(
                    "**🎉 Регистрация завершена успешно!**", reply_markup=kb.main_menu()
                )
                await self.db.populate_fake_tasks(user_id)
                await message.reply(
                    "✨ Мы добавили 5 тестовых задач, чтобы вы могли поближе познакомиться с функционалом нашего бота! 📋\n"
                    "🗑️ Если захотите удалить аккаунт, просто введите команду /delete"
                )

                await self.state.clear(user_id)
            except psycopg.errors.UniqueViolation:
                await message.reply(
                    "Пользователь с таким именем уже существует. Пожалуйста, введите другой логин:"
                )
