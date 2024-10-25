from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List

def task_menu(task_id: int, is_completed: bool) -> InlineKeyboardMarkup:
    """Клавиатура для управления задачей"""
    buttons: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                "Выполнена" if not is_completed else 'Снять отметку',
                callback_data=f'taskstatus_{task_id}'
            )
        ],
        [
            InlineKeyboardButton(
                'Удалить',
                callback_data=f'delete_{task_id}'
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)