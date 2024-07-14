from aiogram import F, Router
from copy import deepcopy
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from Bots.BookBot.database.database import user_dict_template, users_db
from Bots.BookBot.keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from Bots.BookBot.keyboards.pagination_kb import create_pagination
from Bots.BookBot.lexicon.lexicon import LEXICON
from Bots.BookBot.services.file_handling import book
from Bots.BookBot.filters.filters import IsDigitFilter, IsDelBookmarkFilter

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands=['help']))
async def help_answer(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands=['beginning']))
async def beginning_answer(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination('backward',
                                       f'{users_db[message.from_user.id]["page"]} / {len(book)}',
                                       'forward'
                                       ))


@router.message(Command(commands=['continue']))
async def backward_answer(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination('backward',
                                       f'{users_db[message.from_user.id]["page"]} / {len(book)}',
                                       'forward'))


@router.message(Command(commands='bookmarks'))
async def answer_bookmarks(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(*users_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def forward_answer(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination('backward',
                                           f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                                           'forward')
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def backward_answer(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text, reply_markup=create_pagination('backward',
                                         f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                                         'forward'))
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def answer_page(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(users_db[callback.from_user.id]['page'])
    await callback.answer('Страница успешно добавлена в закладки')


@router.callback_query(IsDigitFilter())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination(
            'backward',
            f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]["bookmarks"]
        )
    )


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])


@router.callback_query(IsDelBookmarkFilter())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *users_db[callback.from_user.id]["bookmarks"]
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
