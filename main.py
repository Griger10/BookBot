import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import load_config, Config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)')
    logging.info('Bot started')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers)
    dp.include_router(other_handlers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
