from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


add_sponsor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔐 Majburiy obuna qo'shish", callback_data='add_sponsor'
            )
        ]
    ]
)