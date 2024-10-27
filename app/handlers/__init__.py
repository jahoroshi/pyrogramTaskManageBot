from app.database import db
from app.handlers.registration import RegistrationHandler
from app.handlers.task.task_handler import TaskHandler
from app.states import state

reg_handler = RegistrationHandler(state, db)
task_handler = TaskHandler(state, db)
