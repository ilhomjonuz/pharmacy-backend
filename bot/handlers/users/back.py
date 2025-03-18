from aiogram.fsm.state import State
from aiogram.types import Message
from loader import dp

from bot.buttons.default import menu_markup
from bot.filters import PrivateFilter, AdminFilter


@dp.message(PrivateFilter(), lambda msg: msg.text == "◀️ Orqaga", AdminFilter(), State(None))
async def types_show(msg: Message):
    await msg.answer("Menu", reply_markup=menu_markup)
