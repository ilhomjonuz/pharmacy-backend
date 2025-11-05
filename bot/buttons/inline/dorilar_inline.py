from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ...loader import db


class PillsCallbackData(CallbackData, prefix="pill"):
    dori_id: int
    step: int
    action: str


async def create_dori_callback(dori_id, step=0, action='0'):
    return PillsCallbackData(dori_id=dori_id, step=step, action=action).pack()


async def make_dorilar_list():
    all_dorilar = await db.select_medications()
    CURRENT_LEVEL = 0
    if all_dorilar:
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
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Yopish",
                        callback_data=await create_dori_callback(0, CURRENT_LEVEL - 1)
                    )
                ]
            ]
        )
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


async def have_vidio():
    vidio = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(text='Ha', callback_data='yes'),
                InlineKeyboardButton(text='Yo\'q', callback_data='no')
            ]
        ]
    ).adjust(2).as_markup()
    return vidio


async def get_pill_types():
    pill_types = await db.select_types()
    if pill_types:
        markup = InlineKeyboardBuilder()
        for pill_type in pill_types:
            markup.add(InlineKeyboardButton(text=f"{pill_type[1]}", callback_data=f"type-{pill_type[0]}"))

        return markup.adjust(2).as_markup()
    else:
        return None


async def have_sale():
    markup = InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(text='Mavjud', callback_data='have'),
                InlineKeyboardButton(text='Mavjud emas', callback_data='have not')

            ]
        ]
    ).adjust(2).as_markup()


