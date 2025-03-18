from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.state import State
from typing import Union

from aiogram import F
from aiogram.fsm.context import FSMContext

from bot.buttons.default.menu import doctors_menu
from bot.buttons.inline.doctors_inlines import make_doctors_list, saytda_korinish, DoctorCallbackData, \
    show_doctor_markup
from bot.filters import AdminFilter, PrivateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile

from loader import dp, db, bot

from bot.states.types_states import DoctorsAddStates


@dp.message(PrivateFilter(), lambda msg: msg.text == "👩‍ Doktorlar bo'limi", AdminFilter())
async def doctors_show(msg: Message):
    await msg.answer(msg.text, reply_markup=doctors_menu)


@dp.message(PrivateFilter(), F.text == "➕ Doktor qo'shish", AdminFilter(), State(None))
async def doctors_add(msg: Union[Message, CallbackQuery], state: FSMContext, id=None, ):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("👩‍ Doktorni ism va familiyasini kiriting ", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("👩‍ Doktorni ism va familiyasini kiriting: ", reply_markup=ReplyKeyboardRemove())

    await state.set_state(DoctorsAddStates.fullname)
    await state.set_data({'id': id})


@dp.message(DoctorsAddStates.fullname, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_direction_uz(msg: Message, state: FSMContext):
    await state.update_data({'fullname': msg.text})
    await msg.answer("🇺🇿 Doktor yo'nalishni kiriting: ")
    await state.set_state(DoctorsAddStates.direction_uz)


@dp.message(DoctorsAddStates.direction_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_direction_ru(msg: Message, state: FSMContext):
    await state.update_data({'direction_uz': msg.text})
    await msg.answer("🇷🇺 Doktor yo'nalishni kiriting: ")
    await state.set_state(DoctorsAddStates.direction_ru)


@dp.message(DoctorsAddStates.direction_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_direction_ru(msg: Message, state: FSMContext):
    await state.update_data({'direction_ru': msg.text})
    await msg.answer("🇬🇧 Doktor yo'nalishni kiriting: ")
    await state.set_state(DoctorsAddStates.direction_en)


@dp.message(DoctorsAddStates.direction_en, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_malumoti_uz(msg: Message, state: FSMContext):
    await state.update_data({'direction_en': msg.text})
    await msg.answer("🇺🇿 Ma'lumotlarni kiriting: ")
    await state.set_state(DoctorsAddStates.body_uz)


@dp.message(DoctorsAddStates.body_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_malumoti_ru(msg: Message, state: FSMContext):
    await state.update_data({'body_uz': msg.text})
    await msg.answer("🇷🇺 Ma'lumotlarni kiriting: ")
    await state.set_state(DoctorsAddStates.body_ru)


@dp.message(DoctorsAddStates.body_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_malumoti_ru(msg: Message, state: FSMContext):
    await state.update_data({'body_ru': msg.text})
    await msg.answer("🇬🇧 Ma'lumotlarni kiriting: ")
    await state.set_state(DoctorsAddStates.body_en)


@dp.message(DoctorsAddStates.body_en, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_korinsinmi(msg: Message, state: FSMContext):
    await state.update_data({'body_en': msg.text})
    await msg.answer("📅 Saytda ko'rinsinmi?", reply_markup=await saytda_korinish())
    await state.set_state(DoctorsAddStates.published)


@dp.callback_query(DoctorsAddStates.published)
async def doctor_direction(call: CallbackQuery, state: FSMContext):
    await state.update_data({'published': True if call.data == 'yes' else False})
    await call.message.edit_text("☎️ Doktor raqamini kiriting: ", reply_markup=None)
    await state.set_state(DoctorsAddStates.call)


@dp.message(DoctorsAddStates.call, lambda msg: msg.content_type == ContentType.TEXT)
async def doctor_photo(msg: Message, state: FSMContext):
    await state.update_data({'call': msg.text})
    await msg.answer("🖼 Doktor rasmini kiriting: ")
    await state.set_state(DoctorsAddStates.picture)


@dp.message(PrivateFilter(), DoctorsAddStates.picture, lambda msg: msg.content_type in [ContentType.PHOTO])
async def doctor_add_image(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path  # photos/file_7.jpg
    file_name = f'media/doctors/{file_path}'
    file_name_db = f'doctors/{file_path}'
    downloaded_file = await bot.download_file(file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file.read())

    data = await state.get_data()
    fullname = data['fullname']
    direction_uz = data['direction_uz']
    direction_ru = data['direction_ru']
    direction_en = data['direction_en']
    body_uz = data['body_uz']
    body_ru = data['body_ru']
    body_en = data['body_en']
    published = data['published']
    call = data['call']
    doctor_id = data.get('id')
    if doctor_id:
        await db.update_doctor(fullname, direction_uz, direction_ru, direction_en, call, body_uz, body_ru, body_en,
                               file_name_db, published, doctor_id)
        await msg.answer(f"Doktor muvaffaqiyatli o'zgartirildi!", reply_markup=doctors_menu)
    else:
        await db.doctor_add(fullname, direction_uz, direction_ru, direction_en, call, body_uz, body_ru, body_en,
                            file_name_db, published)
        await msg.answer(f"Doktor muvaffaqiyatli qo'shildi!", reply_markup=doctors_menu)
    await state.clear()


@dp.message(PrivateFilter(), lambda msg: msg.text == "📜 Doktorlar ro'yxati", AdminFilter())
async def doctors_list(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.answer("📜 Doktorlar ro'yxati", reply_markup=await make_doctors_list())
    else:
        await msg.answer(msg.text, reply_markup=await make_doctors_list())


async def delete_doctor(call: CallbackQuery, doctor_id: int):
    await call.message.delete()
    await db.delete_doctor(doctor_id)
    await call.message.answer(f"✅ Doktor muvaffaqiyatli o'chirildi ")


@dp.callback_query(DoctorCallbackData.filter())
async def select_doctor_func(call: CallbackQuery, callback_data: DoctorCallbackData, state: FSMContext):
    doctor_id = callback_data.doctor_id
    step = callback_data.step
    action = callback_data.action
    if step == -1:
        await call.message.delete()
    elif step == 0:
        await call.message.delete()
        await doctors_list(call)
    elif step == 1:
        await call.message.delete()
        await show_detail_doctor(call, doctor_id)
    elif step == 2:
        if action == 'edit':
            await doctors_add(call, state, doctor_id)
        elif action == 'delete':
            await delete_doctor(call, doctor_id)
            await doctors_list(call)
    else:
        await call.message.delete()


async def show_detail_doctor(call, doctor_id):
    doctor = await db.select_doctor(doctor_id)
    image_path = f"media/{doctor[9]}"

    await call.message.answer_photo(FSInputFile(image_path), caption=
    f"Doktor ma'lumoti: \n\n"
    f"Ism-familiya: {doctor[0]}\n"
    f"🇺🇿 Yo'nalishi:  {doctor[1]}\n"
    f"🇷🇺 Yo'nalishi:  {doctor[2]}\n"
    f"🇬🇧 Yo'nalishi:  {doctor[3]}\n"
    f"🇺🇿 Malumoti:  {doctor[4]}\n"
    f"🇷🇺 Malumoti:  {doctor[5]}\n"
    f"🇬🇧 Malumoti:  {doctor[6]}\n"
    f"Saytda ko'rinishi: {'yes' if doctor[8] else 'no'}\n"
    f"Doktor raqami: {doctor[7]}\n",
                                    reply_markup=await show_doctor_markup(doctor_id))


@dp.message(StateFilter(DoctorsAddStates), lambda msg: msg.content_type == ContentType.ANY)
async def delete_msg(msg: Message):
    await msg.delete()
