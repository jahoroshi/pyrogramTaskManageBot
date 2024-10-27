from app.database import Database
from app.handlers.user.base_user_handler import BaseUserHandler
from app.handlers.user.registration_process_handler import RegistrationProcessHandler
from app.handlers.user.start_handler import StartHandler
from app.handlers.user.user_deletion_handler import UserDeletionHandler
from app.states import FSMContext


class UserHandler(StartHandler, RegistrationProcessHandler, UserDeletionHandler):
    """Главный обработчик работы с пользователем."""

    def __init__(self, state: FSMContext, database: Database):
        BaseUserHandler.__init__(self, state, database)
