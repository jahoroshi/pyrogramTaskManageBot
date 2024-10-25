from pyrogram import filters, Client

from app.handlers import reg_handler


@Client.on_message(filters.command("start"))
async def start(client, message):
    await reg_handler.start(client, message)