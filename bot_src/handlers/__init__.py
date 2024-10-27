from bot_src.database import db
from bot_src.handlers.user.user_handler import UserHandler
from bot_src.handlers.task.task_handler import TaskHandler
from bot_src.states import state

user_handler = UserHandler(state, db)
task_handler = TaskHandler(state, db)
