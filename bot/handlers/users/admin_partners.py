from typing import Union

from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from bot.buttons.default import menu_markup
from bot.buttons.default.menu import partners_menu
from bot.buttons.inline import make_partners_list
from bot.buttons.inline.partners_inlines import PartnerCallbackData, show_partner_inline
from bot.filters import AdminFilter, PrivateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import FSInputFile
from loader import dp, db, bot

from bot.states import PartnersAddStates


@dp.message(PrivateFilter(), lambda msg: msg.text == "📁 Hamkorlar", AdminFilter())
async def partners_show(msg: Message):
    await msg.answer(msg.text, reply_markup=partners_menu)


@dp.message(PrivateFilter(), F.text == "➕ Hamkor qo'shish", AdminFilter(), State(None))
async def partner_add_or_edit(msg: Union[Message, CallbackQuery], state: FSMContext, partner_id=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("Hamkorni yangi logotipini yuboring: ", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("Hamkorni logotipini yuboring: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PartnersAddStates.image)
    await state.set_data({'partner_id': partner_id})


@dp.message(PrivateFilter(), PartnersAddStates.image, lambda msg: msg.content_type in [ContentType.PHOTO])
async def partner_add_image(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_name = f'media/partners/{file_path}'
    file_name_db = f'partners/{file_path}'
    downloaded_file = await bot.download_file(file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file.read())

    data = await state.get_data()
    partner_id = data.get('partner_id')
    if partner_id:
        await db.update_partner(partner_id, file_name_db)
        await msg.answer(f"Hamkor muvaffaqiyatli o'zgartirildi!", reply_markup=partners_menu)
    else:
        await db.add_partner(file_name_db)
        await msg.answer(f"Hamkor muvaffaqiyatli qo'shildi!", reply_markup=partners_menu)
    await state.clear()


@dp.message(PrivateFilter(), F.text == "📜 Hamkorlar ro'yxati", AdminFilter())
async def show_partners(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.answer("📜 Hamkorlar ro'yxati", reply_markup=await make_partners_list())
        await call.message.delete()
    else:
        await msg.answer(msg.text, reply_markup=await make_partners_list())


@dp.callback_query(PartnerCallbackData.filter())
async def select_func(call: CallbackQuery, callback_data: PartnerCallbackData, state: FSMContext):
    partner_id = callback_data.partner_id
    step = callback_data.step
    action = callback_data.action
    if step == 0:
        await show_partners(call)
    elif step == 1:
        await show_partner(call, partner_id)
    elif step == 2:
        if action == 'edit':
            await partner_add_or_edit(call, state, partner_id)
        elif action == 'delete':
            await delete_partner(call, partner_id)
            await show_partners(call)
    else:
        await call.message.delete()


# ----------------------------------------------------------EDIT

async def delete_partner(call: CallbackQuery, partner_id: int):
    await db.delete_partner(partner_id)
    await call.message.answer(f"✅ Hamkor muvaffaqiyatli o'chirildi ")


async def show_partner(call, partner_id):
    partner = await db.select_partner(partner_id)
    image_path = f"media/{partner[1]}"
    await call.message.answer_photo(FSInputFile(image_path), caption="Hamkor logosi",
                                    reply_markup=await show_partner_inline(partner_id))
    await call.message.delete()


@dp.message(StateFilter(PartnersAddStates), lambda msg: msg.content_type == ContentType.ANY)
async def delete_msg(msg: Message):
    await msg.delete()
