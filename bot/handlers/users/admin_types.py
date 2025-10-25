from typing import Union

from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from loader import dp, db

from bot.buttons.default import menu_types, categories_menu
from bot.buttons.inline import make_types_list, TypeCallbackData, show_type, show_category
from bot.buttons.inline.types_list_inlines import make_categories_list, CategoryCallbackData
from bot.filters import PrivateFilter, AdminFilter
from bot.states import TypeAddStates, CategoryAddStates


@dp.message(PrivateFilter(), lambda msg: msg.text == "🗒 Dori turlari bo'limi", AdminFilter(), State(None))
async def types_show(msg: Message):
    await msg.answer(msg.text, reply_markup=menu_types)


@dp.message(PrivateFilter(), F.text == "➕ Dori turini qo'shish", AdminFilter(), State(None))
async def type_add(msg: Union[Message, CallbackQuery], state: FSMContext, type_id=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("🇺🇿 Dori turining o'zbekcha nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("🇺🇿 Dori turining o'zbekcha nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TypeAddStates.name_uz)
    await state.set_data({'id': type_id})


@dp.message(TypeAddStates.name_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def type_name_uz(msg: Message, state: FSMContext):
    await state.update_data({'name_uz': msg.text})
    await msg.answer("🇷🇺 Dori turining ruscha nomini kiriting: ")
    await state.set_state(TypeAddStates.name_ru)


@dp.message(TypeAddStates.name_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def type_name_ru(msg: Message, state: FSMContext):
    await state.update_data({'name_ru': msg.text})
    await msg.answer("🇬🇧 Dori turining inglizcha nomini kiriting: ")
    await state.set_state(TypeAddStates.name_en)


@dp.message(TypeAddStates.name_en, lambda msg: msg.content_type == ContentType.TEXT)
async def type_name_ru(msg: Message, state: FSMContext):
    await state.update_data({'name_en': msg.text})
    data = await state.get_data()
    if not data.get('id'):
        await db.add_type(**data)
        await msg.answer("✅ Dori turi muvaffaqiyatli qo'shildi!")
    else:
        await db.update_type(**data)
        await msg.answer("✅ Dori turi muvaffaqiyatli o'zgartirildi!")
    await state.clear()
    await msg.answer("🗒 Dori turlari bo'limi", reply_markup=menu_types)


@dp.message(PrivateFilter(), F.text == "📜 Dori turlari ro'yxati", AdminFilter())
async def types_list(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("📜 Dori turlari ro'yxati", reply_markup=await make_types_list())
    else:
        await msg.answer(msg.text, reply_markup=await make_types_list())


@dp.callback_query(TypeCallbackData.filter())
async def select_func(call: CallbackQuery, callback_data: TypeCallbackData, state: FSMContext):
    type_id = callback_data.type_id
    step = callback_data.step
    action = callback_data.action
    if step == 0:
        await types_list(call)
    elif step == 1:
        await show_type_for_pill(call, type_id)
    elif step == 2:
        if action == 'delete':
            await db.delete_type(type_id)
            await call.message.answer("✅ Dori turi muvaffaqiyatli o'chirildi!")
            await types_list(call)
        elif action == 'edit':
            await type_add(call, state, type_id)
    else:
        await call.message.delete()


async def show_type_for_pill(call, type_id):
    type_obj = await db.select_type(type_id)
    type_info = (f"Dori turi:\n\n"
                 f"🇺🇿 Nomi: {type_obj[1]}\n"
                 f"🇷🇺 Hазвание: {type_obj[2]}\n"
                 f"🇬🇧 Name: {type_obj[3]}")
    await call.message.edit_text(type_info, reply_markup=await show_type(type_id))


@dp.message(StateFilter(TypeAddStates), lambda msg: msg.content_type == ContentType.ANY)
async def delete_msg(msg: Message):
    await msg.delete()


# -------------------------------------------------------------------------------------------


@dp.message(PrivateFilter(), lambda msg: msg.text == "🗂 Kategoriyalar bo'limi", AdminFilter(), State(None))
async def types_show(msg: Message):
    await msg.answer(msg.text, reply_markup=categories_menu)


@dp.message(PrivateFilter(), F.text == "➕ Kategoriya qo'shish", AdminFilter(), State(None))
async def category_add(msg: Union[Message, CallbackQuery], state: FSMContext, category_id=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.delete()
        await call.message.answer("🇺🇿 Dori kategoriyasining o'zbekcha nomini kiriting: ",
                                  reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("🇺🇿 Dori kategoriyasining o'zbekcha nomini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CategoryAddStates.name_uz)
    await state.set_data({'id': category_id})


@dp.message(CategoryAddStates.name_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def category_name_uz(msg: Message, state: FSMContext):
    await state.update_data({'name_uz': msg.text})
    await msg.answer("🇷🇺 Dori kategoriyasining ruscha nomini kiriting: ")
    await state.set_state(CategoryAddStates.name_ru)


@dp.message(CategoryAddStates.name_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def category_name_ru(msg: Message, state: FSMContext):
    await state.update_data({'name_ru': msg.text})
    await msg.answer("🇬🇧 Dori kategoriyasining inglizcha nomini kiriting: ")
    await state.set_state(CategoryAddStates.name_en)


@dp.message(CategoryAddStates.name_en, lambda msg: msg.content_type == ContentType.TEXT)
async def type_name_ru(msg: Message, state: FSMContext):
    await state.update_data({'name_en': msg.text})
    data = await state.get_data()
    if not data.get('id'):
        await db.category_add(**data)
        await msg.answer("✅ Kategoriya muvaffaqiyatli qo'shildi!")
    else:
        print(data)
        await db.update_category(**data)
        await msg.answer("✅ Kategoriya muvaffaqiyatli o'zgartirildi!")
    await state.clear()
    await msg.answer("🗒 Kategoriya bo'limi", reply_markup=categories_menu)


# CategoryTypes
@dp.message(PrivateFilter(), F.text == "📜 Kategoriyalar ro'yxati", AdminFilter())
async def category_list(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("📜 Kategoriyalar ro'yxati", reply_markup=await make_categories_list())
    else:
        await msg.answer(msg.text, reply_markup=await make_categories_list())


# ---------------------------------------------------------------
@dp.callback_query(CategoryCallbackData.filter())
async def select_func(call: CallbackQuery, callback_data: CategoryCallbackData, state: FSMContext):
    category_id = callback_data.category_id
    step = callback_data.step
    action = callback_data.action
    if step == 0:
        await category_list(call)
    elif step == 1:
        await show_category_for_pill(call, category_id)
    elif step == 2:
        if action == 'delete':
            await db.delete_category(category_id)
            await call.message.answer("✅ Kategoriya muvaffaqiyatli o'chirildi!")
            await category_list(call)
        elif action == 'edit':
            await category_add(call, state, category_id)
    else:
        await call.message.delete()


async def show_category_for_pill(call, category_id):
    category_obj = await db.select_category(category_id)
    category_info = (f"Kategoriya:\n\n"
                     f"🇺🇿 Nomi: {category_obj[1]}\n"
                     f"🇷🇺 Hазвание: {category_obj[2]}\n"
                     f"🇬🇧 Name: {category_obj[3]}")
    await call.message.edit_text(category_info, reply_markup=await show_category(category_id))


@dp.message(StateFilter(CategoryAddStates), lambda msg: msg.content_type == ContentType.ANY)
async def delete_msg(msg: Message):
    await msg.delete()
