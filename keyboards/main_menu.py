from aiogram.types import BotCommand
from aiogram import Bot
from Bots.BookBot.lexicon.lexicon import LEXICON


async def set_main_menu(bot: Bot):
    menu = [BotCommand(command=command, description=description) for command, description in LEXICON.items()]
    await bot.set_my_commands(menu)