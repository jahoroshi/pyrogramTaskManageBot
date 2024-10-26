import asyncio

from app.bot import TaskBot, task_bot

if __name__ == "__main__":
    task_bot.run()

# from pyrogram import Client
# from pyrogram.handlers import MessageHandler
#
# from settings import settings
#
#
# async def hello(client, message):
#     print(message)
#     await message.reply('aaa')
#
# app = Client(
#     "my_account",
#     api_id=settings.tg.api_id,
#     api_hash=settings.tg.api_hash,
#     bot_token=settings.tg.bot_token
# )
#
# app.add_handler(MessageHandler(hello))
#
#
#
#
# if __name__ == "__main__":
#     app.run()
