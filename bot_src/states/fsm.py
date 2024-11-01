from typing import Dict, Any, Optional


class State:
    """Базовый класс для всех состояний"""

    def __set_name__(self, owner, name):
        self.owner = owner.__name__
        self.name = name

    def __repr__(self):
        return f"{self.owner}.{self.name}"

    def __eq__(self, other):
        """Метод позволяет сравнивать класс со строкой"""
        if isinstance(other, str):
            return f"{self.owner}.{self.name}" == other
        return NotImplemented


class FSMContext:
    """Контекст FSM для хранения состояния и данных пользователя."""

    def __init__(self) -> None:
        self.states: Dict[int, str] = {}
        self.storage: Dict[int, Any] = {}

    async def set_state(self, user_id: int, state: State) -> None:
        """
        Устанавливает состояние пользователя.
        Ожидает экземпляр State, который выводит ИмяКласса.ИмяПодсостояния.
        """
        if isinstance(state, State):
            self.states[user_id] = repr(state)
        else:
            raise ValueError("Ожидается экземпляр класса State.")

    async def get_state(self, user_id: int) -> str | None:
        """
        Получает состояние пользователя.
        Возвращает строку в формате 'ИмяКласса.ИмяПодсостояния'.
        """
        return self.states.get(user_id)

    async def set_data(self, user_id: int, data: Dict[str, Any]) -> None:
        """Добавление данных пользователя."""
        self.storage[user_id] = data

    async def get_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение данных пользователя."""
        return self.storage.get(user_id)

    async def delete_data(self, user_id: int) -> None:
        """Удаление данных пользователя."""
        self.storage.pop(user_id, None)

    async def clear(self, user_id: int) -> None:
        """Удаляет состояние и данные пользователя."""
        self.states.pop(user_id, None)
        self.storage.pop(user_id, None)
