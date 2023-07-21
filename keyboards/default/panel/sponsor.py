from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


needed = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="🗑 Kanalni o'chirish"
            )
        ],
        [
            KeyboardButton(
                text="◀️ Orqaga"
            )
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)


have_needed = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="➕ Qo'shish"
            ),
            KeyboardButton(
                text="🗑 Kanalni o'chirish"
            )
        ],
        [
            KeyboardButton(
                text="◀️ Orqaga"
            )
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)


back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="◀️ Orqaga"
            )
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)