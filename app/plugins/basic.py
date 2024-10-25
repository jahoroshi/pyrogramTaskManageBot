from pyrogram import filters, Client
from pyrogram.types import CallbackQuery

from app.handlers import reg_handler


@Client.on_message(filters.command("start"))
async def start(client, message):
    await reg_handler.start(client, message)


@Client.on_message(filters.text)
async def text_message(client, message):
    user_id = message.from_user.id
    cur_state = None
    if cur_state:
        if cur_state['state'] in ['registration_name', 'registration_username']:
            await reg_handler.handle_registration(client, message)
        elif cur_state['state'] in ['task_title', 'task_description']:
            ...
    else:
        if message.text == 'Новая задача':
            ...
        elif message.text == 'Задачи':
            ...
        else:
            await message.reply('Команда не распознана. Используйте меню')


@Client.on_callback_query()
async def callback(client: Client, query: CallbackQuery):
    if query.data.startswith('task'):
        ...
