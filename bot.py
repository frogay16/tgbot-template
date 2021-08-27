import asyncpg
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.contrib.fsm_storage.redis import RedisStorage2
from tgbot.utils.register_handlers import register_handlers
from tgbot.data.config import BOT_TOKEN, PG_USERNAME, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB
from tgbot.middlewares.db import DbMiddleware

logger = logging.getLogger(__name__)


async def create_pool(user, password, host, port, dp):
    return await asyncpg.create_pool(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     database=dp
                                     )


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    storage = MemoryStorage()
    #storage = RedisStorage2()

    pool = await create_pool(
        user=PG_USERNAME,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT,
        dp=PG_DB
    )
    bot = Bot(
        token=BOT_TOKEN,
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
