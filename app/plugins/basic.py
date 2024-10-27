from pyrogram import filters

from app.filters import state_filter
from app.handlers import reg_handler, task_handler
from app.states import states as st
from pyrogram import filters

from app.filters import state_filter
from app.handlers import reg_handler, task_handler
from app.states import states as st

"""
Регистрация хендлеров
"""
message_handlers = [
    (reg_handler.start, filters.command("start")),
    (reg_handler.delete, filters.command("delete")),
    (reg_handler.registration, state_filter((st.Registration.name, st.Registration.username))),
    (task_handler.handle_task_creation, state_filter((st.CreateTask.name, st.CreateTask.description))),
    (task_handler.edit_task_handler, state_filter((st.EditTask.name, st.EditTask.description))),
    (task_handler.create_task, filters.regex("Создать задачу")),
    (task_handler.list_tasks, filters.regex("Мои задачи")),
]

callback_query_handlers = [
    (task_handler.handle_status, filters.regex(r"^taskstatus")),
    (task_handler.delete_task, filters.regex(r"^taskdelete")),
    (task_handler.edit_task, filters.regex(r"^edit_task")),
    (task_handler.back_to_taskmenu, filters.regex(r"^back_to_taskmenu")),
]
