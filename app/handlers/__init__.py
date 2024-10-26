from app.handlers.registration import RegistrationHandler
from app.handlers.task import TaskHandler
from app.states import state

reg_handler = RegistrationHandler(state)
task_handler = TaskHandler(state)
