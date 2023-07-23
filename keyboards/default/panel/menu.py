from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

buttons = [
    KeyboardButton(text="📊 Statistika"),
    KeyboardButton(text="🔐 Majburiy obuna")
]

menues = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
menues.add(*buttons)
menues.insert(
    KeyboardButton(text="🗞 Reklama yuborish")
)
menues.add(
    KeyboardButton(text="◀️ Orqaga")
)