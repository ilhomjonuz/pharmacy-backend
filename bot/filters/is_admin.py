from typing import Union

from aiogram import types
from aiogram.filters import BaseFilter

from bot.data import ADMINS


class AdminFilter(BaseFilter):

    async def __call__(self, msg: Union[types.Message, types.CallbackQuery]):
        if isinstance(msg, types.CallbackQuery):
            message = msg.message
        else:
            message = msg
        return f"{message.from_user.id}" in ADMINS
