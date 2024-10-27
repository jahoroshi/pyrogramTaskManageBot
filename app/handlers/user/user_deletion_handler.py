import asyncio

from pyrogram.types import Message

from app.handlers.user.base_user_handler import BaseUserHandler
from app.states.states import Registration


class UserDeletionHandler(BaseUserHandler):
    """Обработчик удаления пользователя."""

    async def delete(self, _, message: Message) -> None:
        user_id = message.from_user.id
        query = "DELETE FROM users WHERE user_id = %s"
        await self.db.execute(query, (user_id,))
        await asyncio.sleep(0.7)
        await message.reply(
            "Пользователь успешно удален. Для продолжения работы с менеджером задач пройдите процедуру регистрации."
        )
        await self.state.set_state(user_id, Registration.name)
        await asyncio.sleep(0.7)
        await message.reply("Введите Ваше имя!")
