from pyrogram import filters, Client
from pyrogram.types import CallbackQuery

from app.handlers import reg_handler, task_handler
from app.states import state


@Client.on_message(filters.command("start"))
async def start(client, message):
    await reg_handler.start(message)


@Client.on_message(filters.text)
async def text_message(client, message):
    user_id = message.from_user.id
    cur_state = await state.get_state(user_id)
    if cur_state:
        if cur_state in ["Registration.name", "Registration_username"]:
            await reg_handler.handle_registration(message)
        elif cur_state in ["CreateTask.name", "CreateTask.description"]:
            await task_handler.handle_task_creation(message)
    else:
        if message.text == "Создать задачу":
            await task_handler.create_task(message)
        elif message.text == "Мои задачи":
            await task_handler.list_tasks(message)
        else:
            await message.reply("Команда не распознана. Используйте меню.")


@Client.on_callback_query()
async def callback(client: Client, query: CallbackQuery):
    if query.data.startswith("taskstatus"):
        await task_handler.handle_status(query)
    elif query.data.startswith('taskdelete'):
        await task_handler.delete_task(query)
