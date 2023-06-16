import asyncio
import logging
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.orm import close_all_sessions
from tgbot.middlewares.db import DBMiddleware
from tgbot.utils import logging
from tgbot.utils.register_handlers import register_handlers
from tgbot.models.config_reader import Settings
from tgbot.models.db.base import create_pool


async def main():
    config = Settings()

    logging.setup(debug=True if config.LOGGING_MODE == "DEBUG" else False)

    logger.warning("Starting bot..")

    bot = Bot(token=config.BOT_TOKEN.get_secret_value(), parse_mode="html")
    dp = Dispatcher(storage=RedisStorage.from_url(config.REDIS_DSN))

    db_middleware = DBMiddleware(create_pool(config.PG_DSN, echo=True if config.LOGGING_MODE == "DEBUG" else False))
    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    register_handlers(dp)

    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types(),
                               config=config
                               )
    finally:
        await dp.storage.close()
        close_all_sessions()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
