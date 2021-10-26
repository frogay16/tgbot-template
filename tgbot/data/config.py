from environs import Env
from os import sep

env = Env()
env.read_env()

# Bot
BOT_TOKEN = env.str("BOT_TOKEN")
# PostgreSQL
PG_USERNAME = env.str("PG_USERNAME")
PG_PASSWORD = env.str("PG_PASSWORD")
PG_HOST = env.str("PG_HOST")
PG_PORT = env.int("PG_PORT")
PG_DB = env.str("PG_DB_NAME")
DB_DUMP_PATH = f"tgbot{sep}data{sep}db_dump.sql"
