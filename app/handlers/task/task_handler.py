from app.database import Database
from app.handlers.task.base_task_handler import BaseTaskHandler
from app.handlers.task.task_creation_handler import TaskCreationHandler
from app.handlers.task.task_editing_handler import TaskEditingHandler
from app.handlers.task.task_status_handler import TaskStatusHandler
from app.handlers.task.task_deletion_handler import TaskDeletionHandler
from app.handlers.task.task_listing_handler import TaskListingHandler
from app.states import FSMContext


class TaskHandler(
    TaskCreationHandler,
    TaskEditingHandler,
    TaskStatusHandler,
    TaskDeletionHandler,
    TaskListingHandler
):
    """Главный обработчик задач, объеденяет весь функционал."""

    def __init__(self, state: FSMContext, database: Database) -> None:
        BaseTaskHandler.__init__(self, state, database)
