from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# For user
buttons = [
    KeyboardButton(text="💰 Hisobim"),
    KeyboardButton(text="🔗 Referal"),
    KeyboardButton(text="📚 Ma'lumot"),
    KeyboardButton(text="📝 Murojaat")
]

start_user = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
start_user.add(
    KeyboardButton(text="➕ Investitsiya kiritish")
)
start_user.add(*buttons)


# For admin
start_admin = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
start_admin.add(
    KeyboardButton(text="➕ Investitsiya kiritish")
)
start_admin.add(*buttons)
start_admin.add(
    KeyboardButton(text="⌨️ Admin panel")
)