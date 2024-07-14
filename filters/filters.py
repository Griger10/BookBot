from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()