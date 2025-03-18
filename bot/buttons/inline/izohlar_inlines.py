from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db, bot


class IzohCallbackData(CallbackData, prefix="izoh"):
    comment_id: int
    step: int
    action: str


async def create_izoh_callback(comment_id, step=0, action='0'):
    return IzohCallbackData(
        comment_id=comment_id, step=step, action=action,
    ).pack()


async def make_izohlar_list():
    all_izoh = await db.select_comments()
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=izoh[1],
                    callback_data=await create_izoh_callback(comment_id=izoh[0], step=CURRENT_LEVEL + 1))
            ] for izoh in all_izoh
        ],
    )
    close_button = InlineKeyboardButton(
        text="❌ Yopish",
        callback_data=await create_izoh_callback(comment_id=0, step=CURRENT_LEVEL - 1, action='close')
    )
    markup.inline_keyboard.append([close_button])
    return markup


async def show_izoh_markup(comment_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_izoh_callback(comment_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_izoh_callback(comment_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_izoh_callback(comment_id, CURRENT_STEP - 1, 'back')
                )
            ]
        ]
    )
    return markup
