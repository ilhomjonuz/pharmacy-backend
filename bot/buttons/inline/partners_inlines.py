from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ...loader import db


class PartnerCallbackData(CallbackData, prefix="partner_callback"):
    partner_id: int
    step: int
    action: str


async def create_partner_callback(image_id, step=0, action='0'):
    return PartnerCallbackData(partner_id=image_id, step=step, action=action).pack()


async def make_partners_list():
    all_partners = await db.select_partners()
    CURRENT_LEVEL = 0
    if all_partners:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"{i}-hamkor",
                        callback_data=await create_partner_callback(all_partners[i - 1][0], CURRENT_LEVEL + 1)
                    )
                ] for i in range(1, len(all_partners) + 1)
            ],
        )
        close_button = InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await create_partner_callback(0, CURRENT_LEVEL - 1)
        )
        markup.inline_keyboard.append([close_button])
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Yopish",
                        callback_data=await create_partner_callback(0, CURRENT_LEVEL - 1)
                    )
                ]
            ]
        )
    return markup


async def show_partner_inline(partner_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_partner_callback(partner_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_partner_callback(partner_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_partner_callback(partner_id, CURRENT_STEP - 1)
                )
            ]
        ]
    )
    return markup
