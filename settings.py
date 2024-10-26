from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    ...

    class Config:
        env_file = ".env"
        extra = "ignore"


class TelegramSettings(BaseSettings):
    api_id: int
    api_hash: str
    bot_token: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    tg: TelegramSettings = TelegramSettings()


settings = Settings()
