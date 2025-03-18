from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


class TypeCallbackData(CallbackData, prefix="type_callback"):
    type_id: int
    step: int
    action: str


async def create_type_callback(type_id, step=0, action='0'):
    return TypeCallbackData(type_id=type_id, step=step, action=action).pack()


async def make_types_list():
    all_types = await db.select_types()
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=type_[1],
                    callback_data=await create_type_callback(type_[0], CURRENT_LEVEL + 1)
                )
            ] for type_ in all_types
        ],
    )
    close_button = InlineKeyboardButton(
        text="❌ Yopish",
        callback_data=await create_type_callback(0, CURRENT_LEVEL - 1)
    )
    markup.inline_keyboard.append([close_button])
    return markup


async def show_type(type_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_type_callback(type_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_type_callback(type_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_type_callback(type_id, CURRENT_STEP - 1)
                )
            ]
        ]
    )
    return markup


class CategoryCallbackData(CallbackData, prefix="category_callback"):
    category_id: int
    step: int
    action: str


async def create_category_callback(category_id, step=0, action='0'):
    return CategoryCallbackData(category_id=category_id, step=step, action=action).pack()


async def make_categories_list():
    all_types = await db.select_categories()
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=type_[1],
                    callback_data=await create_category_callback(type_[0], CURRENT_LEVEL + 1)
                )
            ] for type_ in all_types
        ],
    )
    close_button = InlineKeyboardButton(
        text="❌ Yopish",
        callback_data=await create_category_callback(0, CURRENT_LEVEL - 1)
    )
    markup.inline_keyboard.append([close_button])
    return markup


async def show_category(category_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_category_callback(category_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_category_callback(category_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_category_callback(category_id, CURRENT_STEP - 1)
                )
            ]
        ]
    )
    return markup
