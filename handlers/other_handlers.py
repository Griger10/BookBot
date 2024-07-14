from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def echo(message: Message):
    await message.answer('Данная команда не поддерживается ботом, воспользуйтесь help')
