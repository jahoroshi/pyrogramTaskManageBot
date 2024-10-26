from pyrogram.types import ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    """Создание основного навигационного меню."""
    return ReplyKeyboardMarkup(
        [["Создать задачу", "Мои задачи"]], resize_keyboard=True
    )
