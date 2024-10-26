from typing import Optional, Union, Any
from psycopg_pool import AsyncConnectionPool
from psycopg.sql import LiteralString
from psycopg.rows import dict_row
from psycopg.sql import SQL

from settings import settings





class Database:
    """Класс для взаимодествия с базой данных"""

    def __init__(self) -> None:
        self.pool: Optional[AsyncConnectionPool] = None

    async def connect(self) -> None:
        """Соединение с базой"""
        self.pool = AsyncConnectionPool(
            conninfo=f"host={settings.db.db_host} "
                     f"port={settings.db.db_port} "
                     f"dbname={settings.db.db_name} "
                     f"user={settings.db.db_user} "
                     f"password={settings.db.db_password}",
            min_size=1,
            max_size=10,
            open=True,
            kwargs={'row_factory': dict_row}
        )
        await self.pool.open()
        await self.init_tables()

    async def close(self) -> None:
        """Закрываем соединение"""
        if self.pool:
            await self.pool.close()

    async def init_tables(self) -> None:
        """Инициализация таблиц"""
        if self.pool:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        """
                    CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL
                    )
                    """
                    )
                    await cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS tasks (
                        task_id SERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        is_completed BOOLEAN NOT NULL DEFAULT FALSE,
                        FOREIGN KEY(user_id) REFERENCES users(user_id)
                        )
                        """
                    )
                    await conn.commit()
        else:
            raise ConnectionError('Пул соединений не инициализирован')

    async def execute(self, query: str, params: Union[list, tuple] = ()) -> Any:
        """Выполнение запроса к базе данных. Возвращает результат/результаты"""
        if self.pool:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)
                    if cursor.description:
                        result = await cursor.fetchall()
                    else:
                        result = None
                    await conn.commit()
                    return result
        else:
            raise ConnectionError("Пул соединений не инициализирован.")

    async def get_one(self, query: str, params: Union[tuple, list] = ()) -> Any:
        """Выполнение одного запроса на получение одного элемента."""
        if self.pool:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)
                    result = await cursor.fetchone()
                    return result
        else:
            raise ConnectionError("Пул соединений не инициализирован.")


db = Database()
