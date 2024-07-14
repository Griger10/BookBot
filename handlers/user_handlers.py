from aiogram import F, Router
from copy import deepcopy
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from Bots.BookBot.database.database import user_dict_template, users_db
from Bots.BookBot.keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from Bots.BookBot.keyboards.pagination_kb import create_pagination
from Bots.BookBot.lexicon.lexicon import LEXICON
from Bots.BookBot.services.file_handling import book

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands=['help']))
async def help_answer(message: Message):
    await message.answer(LEXICON[message.text])


