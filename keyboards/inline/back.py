from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


back = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="◀️ Orqaga", callback_data='back'
            )
        ]
    ]
)