from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


class PillsCallbackData(CallbackData, prefix="pill"):
    dori_id: int
    step: int
    action: str


async def create_dori_callback(dori_id, step=0, action='0'):
    return PillsCallbackData(dori_id=dori_id, step=step, action=action).pack()


async def make_dorilar_list():
    all_dorilar = await db.select_medications()
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=type_[1],
                    callback_data=await create_dori_callback(type_[0], CURRENT_LEVEL + 1)
                )
            ] for type_ in all_dorilar
        ],
    )
    close_button = InlineKeyboardButton(
        text="❌ Yopish",
        callback_data=await create_dori_callback(0, CURRENT_LEVEL - 1)
    )
    markup.inline_keyboard.append([close_button])
    return markup


async def show_dori_inline(dori_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_dori_callback(dori_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_dori_callback(dori_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_dori_callback(dori_id, CURRENT_STEP - 1)
                )
            ]
        ]
    )
    return markup
