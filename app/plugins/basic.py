from typing import List, Tuple, Any

from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import CallbackQuery, Message

from app.bot import task_bot
from app.handlers import reg_handler, task_handler
from app.states import state
from app.states.fsm import State
from app.states import states as st


# async def hello(client, message):
#     print(message)
# task_bot.add_handler(MessageHandler(hello))





def filter_state(states: Tuple[Any, Any]):
    async def custom_filter(_, __, message):
        user_id = message.from_user.id
        cur_state = await state.get_state(user_id)
        return cur_state is not None and cur_state in states
    return filters.create(custom_filter)



task_bot.add_handler(MessageHandler(reg_handler.start, filters.command("start") ))

task_bot.add_handler(MessageHandler(reg_handler.registration, filter_state((st.Registration.name, st.Registration.username))))
task_bot.add_handler(MessageHandler(task_handler.handle_task_creation, filter_state((st.CreateTask.name, st.CreateTask.description))))
task_bot.add_handler(MessageHandler(task_handler.edit_task_handler, filter_state((st.EditTask.name, st.EditTask.description))))

task_bot.add_handler(MessageHandler(task_handler.create_task, filters.regex("Создать задачу")))
task_bot.add_handler(MessageHandler(task_handler.list_tasks, filters.regex("Мои задачи")))

task_bot.add_handler(CallbackQueryHandler(task_handler.handle_status, filters.regex(r"^taskstatus")))
task_bot.add_handler(CallbackQueryHandler(task_handler.delete_task, filters.regex(r"^taskdelete")))
task_bot.add_handler(CallbackQueryHandler(task_handler.edit_task, filters.regex(r"^edit_task")))

# async def callback(client: Client, query: CallbackQuery):
#     if query.data.startswith("taskstatus"):
#         await task_handler.handle_status(query)
#     elif query.data.startswith('taskdelete'):
#         await task_handler.delete_task(query)
#     elif query.data.startswith('edit_task'):
#         await query.edit_message_reply_markup()



# # @Client.on_message(filters.command("start"))
# async def start(client, message):
#     await reg_handler.start(message)


# # @Client.on_message(filters.text)
# async def text_message(client, message):
#     user_id = message.from_user.id
#     cur_state = await state.get_state(user_id)
#     if cur_state:
#         if cur_state in [Registration.name, Registration.username]:
#             await reg_handler.registration(message)
#         elif cur_state in [CreateTask.name, CreateTask.description]:
#             await task_handler.handle_task_creation(message)
#     else:
#         if message.text == "Создать задачу":
#             await task_handler.create_task(message)
#         elif message.text == "Мои задачи":
#             await task_handler.list_tasks(message)
#         else:
#             await message.reply("Команда не распознана. Используйте меню.")


# @Client.on_callback_query()
