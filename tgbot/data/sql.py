import asyncio
import asyncpg
from config_reader import config


async def create_db():
    create_db_command = open(config.DB_DUMP_PATH, "r", encoding="utf-8").read()
    conn: asyncpg.Connection = await asyncpg.connect(user=config.PG_USERNAME,
                                                     password=config.PG_PASSWORD.get_secret_value(),
                                                     host=config.PG_HOST,
                                                     port=config.PG_PORT,
                                                     database=config.PG_DB
                                                     )
    await conn.execute(create_db_command)
    await conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
