from app.database import db
from app.handlers.user.user_handler import UserHandler
from app.handlers.task.task_handler import TaskHandler
from app.states import state

user_handler = UserHandler(state, db)
task_handler = TaskHandler(state, db)
