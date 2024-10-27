import os

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        extra = "ignore"


class TelegramSettings(BaseSettings):
    api_id: int
    api_hash: str
    bot_token: str

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        extra = "ignore"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    tg: TelegramSettings = TelegramSettings()


settings = Settings()
