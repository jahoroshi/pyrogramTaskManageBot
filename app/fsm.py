from typing import Dict, Any


class FSMContext:
    """Контекст FSM для хранения состояния и данных пользователя."""

    def __init__(self) -> None:
        self.states: Dict[int, str] = {}
        self.storage: Dict[int, Any] = {}

    def set_state(self, user_id: int, state: str) -> None:
        """Устанавливает состояние пользователя."""
        self.states[user_id] = state

    def get_state(self, user_id: int) -> Dict[str, Any] | None:
        """Получает состояние пользователя."""
        return self.states.get(user_id)

    def set_data(self, user_id: int, data: Dict[str, Any]) -> None:
        """Добавление данных пользователя"""
        self.storage[user_id] = data

    def get_data(self, user_id: int) -> Dict[str, Any]:
        """Получение данных пользователя"""
        return self.storage.get(user_id)

    def delete_data(self, user_id: int) -> None:
        """Удаление данных"""
        self.storage.pop(user_id)
    def clear(self, user_id: int) -> None:
        """Удаляет состояние пользователя."""
        self.states.pop(user_id, None)