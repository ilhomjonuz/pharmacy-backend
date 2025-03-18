import re

from aiogram.enums import ContentType
from aiogram.fsm.state import State
from typing import Union

from aiogram import F
from aiogram.fsm.context import FSMContext

from bot.buttons.default import dorilar_menu
from bot.buttons.default.menu import doctors_menu
from bot.buttons.inline import show_dori_inline
from bot.buttons.inline.dorilar_inline import PillsCallbackData, make_dorilar_list
from bot.filters import AdminFilter, PrivateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile

from loader import dp, db, bot

from bot.states.types_states import PillsAddStates


@dp.message(PrivateFilter(), lambda msg: msg.text == "💊 Dorilar bo'limi", AdminFilter())
async def doctors_show(msg: Message):
    await msg.answer(msg.text, reply_markup=dorilar_menu)


@dp.message(PrivateFilter(), F.text == "➕ Dori qo'shish", AdminFilter(), State(None))
async def dori_name_add(msg: Union[Message, CallbackQuery], state: FSMContext, id=None, ):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("🇺🇿 Dori nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("🇺🇿 Dori nomini kiriting: ", reply_markup=ReplyKeyboardRemove())

    await state.set_state(PillsAddStates.name_uz)
    await state.set_data({'id': id})


@dp.message(PillsAddStates.name_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_malumot_uz(msg: Message, state: FSMContext):
    await state.update_data({'name_uz': msg.text})
    await msg.answer("🇷🇺 Dori nomini kiriting: ")
    await state.set_state(PillsAddStates.name_ru)


@dp.message(PillsAddStates.name_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_malumot_uz(msg: Message, state: FSMContext):
    await state.update_data({'name_ru': msg.text})
    await msg.answer("🇬🇧 Dori nomini kiriting: ")
    await state.set_state(PillsAddStates.name_en)


@dp.message(PillsAddStates.name_en, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_malumot_uz(msg: Message, state: FSMContext):
    await state.update_data({'name_en': msg.text})
    await msg.answer("🇺🇿 Dori haqida malumot kiriting: ")
    await state.set_state(PillsAddStates.information_dori_uz)


@dp.message(PillsAddStates.information_dori_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_malumot_ru(msg: Message, state: FSMContext):
    await state.update_data({'information_dori_uz': msg.text})
    await msg.answer("🇷🇺 Dori haqida malumot kiriting: ")
    await state.set_state(PillsAddStates.information_dori_ru)


@dp.message(PillsAddStates.information_dori_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_malumot_en(msg: Message, state: FSMContext):
    await state.update_data({'information_dori_ru': msg.text})
    await msg.answer("🇬🇧 Dori haqida malumot kiriting: ")
    await state.set_state(PillsAddStates.information_dori_en)


@dp.message(PillsAddStates.information_dori_en, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_narxi(msg: Message, state: FSMContext):
    await state.update_data({'information_dori_en': msg.text})
    await msg.answer("💰 Dori narxini kiriting: ")
    await state.set_state(PillsAddStates.narxi)


@dp.message(PillsAddStates.narxi, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_tarkibi_uz(msg: Message, state: FSMContext):
    await state.update_data({'price': msg.text})
    await msg.answer("🇺🇿 Dori tarkibini kiriting: ")
    await state.set_state(PillsAddStates.tarkibi_uz)


@dp.message(PillsAddStates.tarkibi_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_tarkibi_ru(msg: Message, state: FSMContext):
    await state.update_data({'tarkibi_uz': msg.text})
    await msg.answer("🇷🇺 Dori tarkibini kiriting: ")
    await state.set_state(PillsAddStates.tarkibi_ru)


@dp.message(PillsAddStates.tarkibi_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_tarkibi_en(msg: Message, state: FSMContext):
    await state.update_data({'tarkibi_ru': msg.text})
    await msg.answer("🇬🇧 Dori tarkibini kiriting: ")
    await state.set_state(PillsAddStates.tarkibi_en)


@dp.message(PillsAddStates.tarkibi_en, lambda msg: msg.content_type == ContentType.TEXT)
async def dori_muddati(msg: Message, state: FSMContext):
    await state.update_data({'tarkibi_en': msg.text})
    await msg.answer("📆 Dori yaroqlilik muddati\n"
                     "(Misol uchun: 2025-12-31) ")
    await state.set_state(PillsAddStates.yaroqlilik_muddati)


@dp.message(PillsAddStates.yaroqlilik_muddati, lambda msg: msg.content_type == ContentType.TEXT and re.match(r"^\d{4}-\d{2}-\d{2}$", msg.text))
async def doctor_photo(msg: Message, state: FSMContext):
    await state.update_data({'yaroqlilik_muddati': msg.text})
    await msg.answer("🖼 Dori rasmini kiriting: ")
    await state.set_state(PillsAddStates.rasmi)


@dp.message(PrivateFilter(), PillsAddStates.rasmi, lambda msg: msg.content_type in [ContentType.PHOTO])
async def dori_add_image(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_name = f'media/pills/{file_path}'
    file_name_db = f'pills/{file_path}'
    downloaded_file = await bot.download_file(file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file.read())
    data = await state.get_data()

    if not data.get('id'):
        await db.add_medication(
            name_uz=data['name_uz'],
            name_ru=data['name_ru'],
            name_en=data['name_en'],
            body_uz=data['information_dori_uz'],
            body_ru=data['information_dori_ru'],
            body_en=data['information_dori_en'],
            price=data['price'],
            information_uz=data['tarkibi_uz'],
            information_ru=data['tarkibi_ru'],
            information_en=data['tarkibi_en'],
            expiration_date=data['yaroqlilik_muddati'],
            picture=file_name_db
        )
        await msg.answer("✅ Dori muvaffaqiyatli qo'shildi!")
    else:
        await db.update_medication(
            id=data['id'],
            name_uz=data['name_uz'],
            name_ru=data['name_ru'],
            name_en=data['name_en'],
            body_uz=data['information_dori_uz'],
            body_ru=data['information_dori_ru'],
            body_en=data['information_dori_en'],
            price=data['price'],
            information_uz=data['tarkibi_uz'],
            information_ru=data['tarkibi_ru'],
            information_en=data['tarkibi_en'],
            expiration_date=data['yaroqlilik_muddati'],
            picture=file_name_db
        )
        await msg.answer("✅ Dori muvaffaqiyatli yangilandi!")

    await state.clear()
    await msg.answer("💊 Dorilar bo'limi", reply_markup=dorilar_menu)


# --------------------------------------------------------------->

@dp.message(PrivateFilter(), F.text == "📜 Dorilar ro'yxati", AdminFilter())
async def show_dorilar(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.answer("📜 Dorilar ro'yxati", reply_markup=await make_dorilar_list())
        await call.message.delete()
    else:
        await msg.answer(msg.text, reply_markup=await make_dorilar_list())


@dp.callback_query(PillsCallbackData.filter())
async def select_func(call: CallbackQuery, callback_data: PillsCallbackData, state: FSMContext):
    dori_id = callback_data.dori_id
    step = callback_data.step
    action = callback_data.action
    if step == 0:
        await show_dorilar(call)
    elif step == 1:
        await show_pill_info(call, dori_id)
    elif step == 2:
        if action == 'edit':
            await dori_name_add(call, state, dori_id)
        elif action == 'delete':
            await delete_dori(call, dori_id)
    else:
        await call.message.delete()


async def show_pill_info(call: CallbackQuery, dori_id):
    dori = await db.select_medication(dori_id)
    dori_info = (f"Dori haqida ma'lumot:\n\n"
                 f"🇺🇿 Nomi: {dori[1]}\n"
                 f"🇷🇺 Название: {dori[2]}\n"
                 f"🇬🇧 Name: {dori[3]}\n"
                 f"💰 Narxi: {dori[4]}\n"
                 f"🇺🇿 Tarkibi: {dori[5]}\n"
                 f"📆 Yaroqlilik muddati: {dori[5]}")
    image = f"media/{dori[6]}"
    try:
        await call.message.answer_photo(FSInputFile(image), caption=dori_info, reply_markup=await show_dori_inline(dori_id))
        await call.message.delete()
    except Exception as err:
        await call.message.edit_text(dori_info, reply_markup=await show_dori_inline(dori_id))


async def delete_dori(call: CallbackQuery, dori_id: int):
    await call.message.delete()
    await db.delete_medication(dori_id)
    await call.message.answer(f"✅ Dori muvaffaqiyatli o'chirildi ")
