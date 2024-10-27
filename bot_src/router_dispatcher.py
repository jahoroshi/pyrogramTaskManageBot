from pyrogram import filters

from bot_src.filters import state_filter
from bot_src.handlers import user_handler, task_handler
from bot_src.states import states as st

"""
Регистрация хендлеров по спискам. Каждый список должен именоваться как класс из pyrogram.handlers в snake_case.

Шаблон:
имя_класса = [
    (метод обработчика, фильтр),
]

"""
message_handlers = [
    (user_handler.start, filters.command("start")),
    (user_handler.delete, filters.command("delete")),
    (
        user_handler.registration,
        state_filter((st.Registration.name, st.Registration.username)),
    ),
    (
        task_handler.handle_task_creation,
        state_filter((st.CreateTask.name, st.CreateTask.description)),
    ),
    (
        task_handler.edit_task_handler,
        state_filter((st.EditTask.name, st.EditTask.description)),
    ),
    (task_handler.create_task, filters.regex("Создать задачу")),
    (task_handler.list_tasks, filters.regex("Мои задачи")),
]

callback_query_handlers = [
    (task_handler.handle_status, filters.regex(r"^taskstatus")),
    (task_handler.delete_task, filters.regex(r"^taskdelete")),
    (task_handler.edit_task, filters.regex(r"^edit_task")),
    (task_handler.back_to_taskmenu, filters.regex(r"^back_to_taskmenu")),
]
