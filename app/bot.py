# import psutil
import os
import sys
import importlib
from pyrogram import Client, enums, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from pyrogram.types import Message

from app.database import Database, db
from app.handlers import reg_handler
from settings import settings



class TaskBot(Client):
    """
    Главный класс Telegram-бота.
    Управляет запуском/остановкой/перезапуском бота
    Автоматически регистрирует списки хэндлеров
    """

    def __init__(self):
        config = settings.tg

        super().__init__(
            "task_manager_bot",
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
            parse_mode=enums.ParseMode.MARKDOWN,
            plugins=dict(root="app.plugins")
        )
        self.db: Database = db
        self.routers_path = 'app.plugins.basic' #Маршрут к дериктории со списками хэндлеров

    async def start(self):
        """Запускает бота и подключается к базе данных."""
        await super().start()
        await self.db.connect()

        # Запускает регистрацию хэндлеров
        await self._register_handlers()
        me = await self.get_me()
        print(f"Бот @{me.username} запущен.")



    async def stop(self):
        await self.db.close()
        await super().stop()
        print("Task Stopped.")

    async def restart(self):
        await self.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    async def _register_handlers(self):
        # Получаем импорт файла, содержащего список хэндлеров
        router_module = importlib.import_module(self.routers_path)

        # Получаем список кортежей, каждый кортеж содержит имя атрибута и его значение,
        # учитываются только атрибуты-списки, оканчивающиеся на 'handlers'
        handler_lists = [
            (attr, getattr(router_module, attr)) for attr in dir(router_module)
            if isinstance(getattr(router_module, attr), list) and attr.endswith('handlers')
        ]

        for handler_list_name, handlers in handler_lists:
            # Создается имя метода регистрации по имени списка хэндлеров
            method_name = f"register_{handler_list_name}"
            # Получаем метод регистрации хэндлера из класса бота (TaskBot)
            registration_method = getattr(self, method_name, None)
            if registration_method and callable(registration_method):
                registration_method(handlers)
            else:
                print(f"Метод регистрации '{method_name}' не найден в классе TaskBot.")


    # Отдельные методы для регистрации хэндлеров
    def register_message_handlers(self, handlers):
        for handler_func, filter in handlers:
            self.add_handler(MessageHandler(handler_func, filter))

    def register_callback_query_handlers(self, handlers):
        for handler_func, filter in handlers:
            self.add_handler(CallbackQueryHandler(handler_func, filter))
    #
    # def register_edited_message_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(EditedMessageHandler(handler_func, filter))
    #
    # def register_deleted_message_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(DeletedMessagesHandler(handler_func, filter))
    #
    # def register_inline_query_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(InlineQueryHandler(handler_func, filter))
    #
    # def register_chosen_inline_result_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(ChosenInlineResultHandler(handler_func, filter))
    #
    # def register_chat_member_updated_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(ChatMemberUpdatedHandler(handler_func, filter))
    #
    # def register_user_status_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(UserStatusHandler(handler_func, filter))
    #
    # def register_poll_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(PollHandler(handler_func, filter))
    #
    # def register_disconnect_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(DisconnectHandler(handler_func, filter))
    #
    # def register_raw_update_handlers(self, handlers):
    #     for handler_func, filter in handlers:
    #         self.add_handler(RawUpdateHandler(handler_func, filter))


task_bot = TaskBot()