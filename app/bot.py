# import psutil
import os
import sys

from pyrogram import Client
from pyrogram.types import Message

from settings import settings


class TaskBot(Client):
    """Класс Telegram-бота для управления задачами."""
    def __init__(self):
        config = settings.tg

        super().__init__(
            'task_manager_bot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
            plugins=dict(root="app.plugins")
        )
        # self.db: Database = Database()

    async def start(self):
        """Запускает бота и подключается к базе данных."""
        await super().start()
        # await self.db.connect()
        me = await self.get_me()
        print(f"Бот @{me.username} запущен.")

    async def stop(self):
        # await self.db.close()
        await super().stop()
        print("Task Stopped.")

    async def restart(self):
        await self.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # @staticmethod
    # async def extract_command_text(message: Message):
    #     """
    #     Extracts the command text from the message.
    #     """
    #     cmd = message.command
    #     return " ".join(cmd[1:]) if len(cmd) > 1 else None
