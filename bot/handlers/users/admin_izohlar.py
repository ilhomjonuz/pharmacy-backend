from typing import Union

from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import dp, db

from bot.buttons.default.menu import izohlar_menu
from bot.buttons.inline import make_izohlar_list
from bot.buttons.inline.izohlar_inlines import IzohCallbackData, show_izoh_markup
from bot.filters import PrivateFilter, AdminFilter
from bot.states import IzohlarAddStates


@dp.message(PrivateFilter(), lambda msg: msg.text == "💬 Izohlar", AdminFilter(), State(None))
async def izohlar_show(msg: Message):
    await msg.answer(msg.text, reply_markup=izohlar_menu)


@dp.message(PrivateFilter(), F.text == "➕ Izoh qo'shish", AdminFilter(), State(None))
async def izoh_add(msg: Union[Message, CallbackQuery], state: FSMContext, body=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("💬 Izohni kiriting: ", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("💬 Izohni kiriting:  ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(IzohlarAddStates.body)
    await state.set_data({'id': body})


@dp.message(IzohlarAddStates.body, lambda msg: msg.content_type == ContentType.TEXT)
async def izoh_avtori(msg: Message, state: FSMContext):
    await state.update_data({'body': msg.text})
    await msg.answer("🙎‍ Izoh avtorini kiriting: ")
    await state.set_state(IzohlarAddStates.avtor)


@dp.message(IzohlarAddStates.avtor, lambda msg: msg.content_type == ContentType.TEXT)
async def izoh_qoshildi(msg: Message, state: FSMContext):
    await state.update_data({'avtor': msg.text})
    data = await state.get_data()
    if not data.get('id'):
        await db.add_izoh(data['avtor'], data['body'])
        await msg.answer("✅ Izoh muvaffaqiyatli qo'shildi!")
    else:
        await db.update_izoh(data['id'], data['avtor'], data['body'])
        await msg.answer("✅ Izoh muvaffaqiyatli yangilandi!")
    await state.clear()
    await msg.answer("💬 Izohlar", reply_markup=izohlar_menu)


@dp.message(PrivateFilter(), lambda msg: msg.text == "📜 Izohlar ro'yxati", AdminFilter())
async def izohlar_list(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("📜 Izohlar ro'yxati", reply_markup=await make_izohlar_list())
    else:
        await msg.answer(msg.text, reply_markup=await make_izohlar_list())


@dp.callback_query(IzohCallbackData.filter())
async def select_func(call: CallbackQuery, callback_data: IzohCallbackData, state: FSMContext):
    comment_id = callback_data.comment_id
    step = callback_data.step
    action = callback_data.action
    if step == 0:
        await izohlar_list(call)
    elif step == 1:
        await show_izoh(call, comment_id)
    elif step == 2:
        if action == 'delete':
            await db.delete_izoh(comment_id)
            await call.message.answer("✅ Izoh muvaffaqiyatli o'chirildi!")
            await izohlar_list(call)
        elif action == 'edit':
            await izoh_add(call, state, comment_id)
    else:
        await call.message.delete()


async def show_izoh(call, comment_id):
    comment = await db.select_izoh(comment_id)
    comment_text = (f"Izoh:\n\n"
                    f"🙎‍ Avtor: {comment[1]}\n"
                    f"💬 Izoh: {comment[2]}\n"
                    f"📅 Yozilgan sana: {comment[3]}")
    await call.message.edit_text(comment_text, reply_markup=await show_izoh_markup(comment_id))
