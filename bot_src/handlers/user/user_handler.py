from bot_src.database import Database
from bot_src.handlers.user.base_user_handler import BaseUserHandler
from bot_src.handlers.user.registration_process_handler import (
    RegistrationProcessHandler,
)
from bot_src.handlers.user.start_handler import StartHandler
from bot_src.handlers.user.user_deletion_handler import UserDeletionHandler
from bot_src.states import FSMContext


class UserHandler(StartHandler, RegistrationProcessHandler, UserDeletionHandler):
    """Главный обработчик работы с пользователем."""

    def __init__(self, state: FSMContext, database: Database):
        BaseUserHandler.__init__(self, state, database)
