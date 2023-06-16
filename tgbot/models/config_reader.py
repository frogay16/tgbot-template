from pydantic import BaseSettings, SecretStr, RedisDsn, PostgresDsn


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    PG_DSN: PostgresDsn
    REDIS_DSN: RedisDsn
    LOGGING_MODE: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
