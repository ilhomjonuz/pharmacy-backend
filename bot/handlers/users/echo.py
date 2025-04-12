from aiogram.fsm.state import State
from aiogram.types import Message
from loader import dp

from bot.filters import PrivateFilter, AdminFilter


@dp.message(PrivateFilter(), AdminFilter(), State(None))
async def types_show(msg: Message):
    await msg.answer(msg.text)
