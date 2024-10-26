from dataclasses import dataclass


@dataclass
class User:
    """Модель пользователей"""

    user_id: int
    name: str
    username: str


@dataclass
class Task:
    """Модель задачей"""

    task_id: int
    user_id: int
    name: str
    description: str
    is_completed: bool
