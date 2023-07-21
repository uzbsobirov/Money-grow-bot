from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
back.add(
    KeyboardButton(
        text="◀️ Orqaga"
    )
)