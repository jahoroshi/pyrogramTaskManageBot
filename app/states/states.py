from app.states.fsm import State

"""Статусы для FSMContext"""


class CreateTask:
    name = State()
    description = State()


class Registration:
    name = State()
    username = State()
