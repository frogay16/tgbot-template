from pydantic import BaseSettings, SecretStr
from os import sep


class Settings(BaseSettings):
    BOT_TOKEN: str

    # PostgreSQL
    PG_USERNAME: str
    PG_PASSWORD: SecretStr
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    DB_DUMP_PATH = f"tgbot{sep}data{sep}db_dump.sql"

    # REDIS
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr
    REDIS_DB_FSM: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
