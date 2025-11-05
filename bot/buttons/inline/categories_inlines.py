from loader import db
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def get_categories():
    categories = await db.select_categories()
    if categories:
        send_categories = InlineKeyboardBuilder()
        for category in categories:
            send_categories.add(
                InlineKeyboardButton(
                text=category[1],
                callback_data=f"cat-{category[0]}"
                )
            )
        return send_categories.adjust(2).as_markup()

    else:
        return None