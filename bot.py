import asyncpg
import asyncio
import logging
from loguru import logger
from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.data.config_reader import config
from tgbot.middlewares.db import DbMiddleware
from tgbot.utils import logging
from tgbot.utils.register_handlers import register_handlers


async def main():
    logging.setup()
    logger.error("Starting bot..")

    try:
        pool = await asyncpg.create_pool(
            user=config.PG_USERNAME,
            password=config.PG_PASSWORD.get_secret_value(),
            host=config.PG_HOST,
            port=config.PG_PORT,
            database=config.PG_DB
        )
    except ConnectionRefusedError:
        logger.critical("[-] Connection to PostrgeSQL DB - FAILURE - abort the startup...")
        return
    else:
        logger.success("[+] Connection to PostrgeSQL DB - SUCCESSFULLY")

    # storage = MemoryStorage()
    storage = RedisStorage2(
        db=config.REDIS_DB_FSM,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD.get_secret_value()
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode="html"
    )
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    register_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
