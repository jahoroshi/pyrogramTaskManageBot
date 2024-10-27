from bot_src.states.fsm import State

"""Статусы для FSMContext"""


class CreateTask:
    name = State()
    description = State()


class Registration:
    name = State()
    username = State()


class EditTask:
    name = State()
    description = State()
