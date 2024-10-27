from pyrogram.types import Message

import bot_src.keyboards as kb
from bot_src.handlers.user.base_user_handler import BaseUserHandler
from bot_src.states.states import Registration


class StartHandler(BaseUserHandler):
    """Обработчик команды /start."""

    async def start(self, _, message: Message) -> None:
        user_id: int = message.from_user.id
        user = await self._get_user(user_id)
        if user is None:
            await self.state.set_state(user_id, Registration.name)
            await message.reply("Введите имя!")
        else:
            await message.reply("С возвращением!", reply_markup=kb.main_menu())
