from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List


def task_menu(task_id: int, is_completed: bool) -> InlineKeyboardMarkup:
    """Клавиатура для управления задачей"""
    buttons: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                "Задача выполнена" if not is_completed else "Снять отметку",
                callback_data=f"taskstatus_{task_id}",
            )
        ],
        [
            InlineKeyboardButton("Изменить", callback_data=f"edit_task_{task_id}"),
            InlineKeyboardButton("Удалить", callback_data=f"taskdelete_{task_id}"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def task_edit_name_discr(task_id: int) -> InlineKeyboardMarkup:
    buttons: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                "Изменить название", callback_data=f"edit_task_name_{task_id}"
            ),
            InlineKeyboardButton(
                "Изменить описание", callback_data=f"edit_task_disc_{task_id}"
            ),
        ],
        [
            InlineKeyboardButton("Назад", callback_data=f"back_to_taskmenu_{task_id}"),
        ],
    ]
    return InlineKeyboardMarkup(buttons)
