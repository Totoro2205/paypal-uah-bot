import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.config.config import settings
from bot.utils.logger import logger
from bot.utils.bot_utils import identify_myself, set_commands, on_startup, on_shutdown
from bot.handlers.commands import commands_router
from bot.handlers.messages import messages_router
from bot.middlewares.antiflood import AntiFloodMiddleware
from bot.workers.rates import rates_worker


async def main() -> None:

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await set_commands(bot=bot)

    try:
        dp = Dispatcher()
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        dp.message.middleware(AntiFloodMiddleware(1))
        dp.include_routers(commands_router, messages_router)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"Bot started from <y>{await identify_myself()}</y>")
        logger.info(f"Project path: {settings.PROJECT_ROOT}")
        await asyncio.gather(rates_worker(), dp.start_polling(bot))
        # await dp.start_polling(bot)
    except Exception as _ex:
        logger.error(f"Bot error! {repr(_ex)}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    if not os.path.exists(path=settings.PROJECT_TEMP):
        os.mkdir(path=settings.PROJECT_TEMP)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as _ex:
        logger.critical(f"Can't run the bot! {repr(_ex)}")
    finally:
        logger.info("Bot stopped!")
        exit(0)
