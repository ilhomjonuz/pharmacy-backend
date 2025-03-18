from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db, bot


class DoctorCallbackData(CallbackData, prefix="doctor_callback"):
    doctor_id: int
    step: int
    action: str


async def create_doctor_callback(doctor_id, step=0, action='0'):
    return DoctorCallbackData(
        doctor_id=doctor_id, step=step, action=action,
    ).pack()


async def make_doctors_list():
    all_doctors = await db.select_doctors()
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=doctor[1],
                    callback_data=await create_doctor_callback(doctor_id=doctor[0], step=CURRENT_LEVEL + 1))
            ] for doctor in all_doctors
        ],
    )
    close_button = InlineKeyboardButton(
        text="❌ Yopish",
        callback_data=await create_doctor_callback(doctor_id=0, step=CURRENT_LEVEL - 1, action='close')
    )
    markup.inline_keyboard.append([close_button])
    return markup


async def show_doctor_markup(doctor_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=await create_doctor_callback(doctor_id, CURRENT_STEP + 1, 'delete')
                ),
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=await create_doctor_callback(doctor_id, CURRENT_STEP + 1, 'edit')
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data=await create_doctor_callback(doctor_id, CURRENT_STEP - 1, 'back')
                )
            ]
        ]
    )
    return markup


async def saytda_korinish():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha",
                    callback_data='yes'
                ),
                InlineKeyboardButton(
                    text="🚫 Yo'q",
                    callback_data='no'
                ),
            ]
        ]
    )
    return markup
