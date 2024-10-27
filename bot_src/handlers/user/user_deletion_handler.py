import asyncio

import psycopg
from pyrogram.types import Message

from bot_src.handlers.user.base_user_handler import BaseUserHandler
from bot_src.states.states import Registration


class UserDeletionHandler(BaseUserHandler):
    """Обработчик удаления пользователя."""

    async def delete(self, _, message: Message) -> None:
        user_id = message.from_user.id
        query = "DELETE FROM users WHERE user_id = %s"
        try:
            await self.db.execute(query, (user_id,))
        except psycopg.Error:
            await message.reply(
                "Произошла ошибка, попробуйте еще раз."
            )
            return

        await asyncio.sleep(0.7)
        await message.reply(
            "Пользователь успешно удален. Для продолжения работы с менеджером задач пройдите процедуру регистрации."
        )
        await self.state.set_state(user_id, Registration.name)
        await asyncio.sleep(0.7)
        await message.reply("Введите Ваше имя!")
