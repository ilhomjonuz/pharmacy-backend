from typing import Union

from aiogram import types
from aiogram.filters import BaseFilter


class PrivateFilter(BaseFilter):

    async def __call__(self, msg: Union[types.Message, types.CallbackQuery]):
        if isinstance(msg, types.CallbackQuery):
            message = msg.message
        else:
            message = msg
        return message.chat.type == 'private'
