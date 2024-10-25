from pyrogram import filters, Client

@Client.on_message(filters.text & filters.incoming)
async def reply_to_all(client, message):
    await message.reply("Привет! Это автоответ.")