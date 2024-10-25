# import psutil
from pyrogram import Client
from pyrogram.types import Message

from settings import settings


class TaskBot(Client):
    def __init__(self):
        config = settings.tg

        super().__init__(
            'taskBot',
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
            plugins=dict(root="app.plugins")
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"TaskBot started on @{me.username}.")

    async def stop(self):
        await super().stop()
        print("Task Stopped.")

    async def restart(self):
        await self.stop()

        # try:
        #     process = psutil.Process(os.getpid())
        #     for handler in process.open_files() + process.connections():
        #         os.close(handler.fd)
        # except Exception as e:
        #     print(e)
        #
        # os.execl(sys.executable, sys.executable, "-m", __name__)
        # sys.exit()

    @staticmethod
    async def extract_command_text(message: Message):
        """
        Extracts the command text from the message.
        """
        cmd = message.command
        return " ".join(cmd[1:]) if len(cmd) > 1 else None
