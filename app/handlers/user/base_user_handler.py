from app.database import Database
from app.models import User
from app.states import FSMContext


class BaseUserHandler:
    """Базовый класс для обработки действий с пользователем."""

    def __init__(self, state: FSMContext, database: Database):
        self.state: FSMContext = state
        self.db: Database = database

    async def _get_user(self, user_id: int) -> User | None:
        """Получает пользователя из базы данных."""
        query = "SELECT * FROM users WHERE user_id = %s"
        data = await self.db.get_one(query, (user_id,))
        if data:
            return User(**data)
        return None
