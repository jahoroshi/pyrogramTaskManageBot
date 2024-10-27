from bot_src.database import Database
from bot_src.handlers.task.base_task_handler import BaseTaskHandler
from bot_src.handlers.task.task_creation_handler import TaskCreationHandler
from bot_src.handlers.task.task_editing_handler import TaskEditingHandler
from bot_src.handlers.task.task_status_handler import TaskStatusHandler
from bot_src.handlers.task.task_deletion_handler import TaskDeletionHandler
from bot_src.handlers.task.task_listing_handler import TaskListingHandler
from bot_src.states import FSMContext


class TaskHandler(
    TaskCreationHandler,
    TaskEditingHandler,
    TaskStatusHandler,
    TaskDeletionHandler,
    TaskListingHandler,
):
    """Главный обработчик задач, объеденяет весь функционал."""

    def __init__(self, state: FSMContext, database: Database) -> None:
        BaseTaskHandler.__init__(self, state, database)
