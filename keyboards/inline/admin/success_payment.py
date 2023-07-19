from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_check_payment(user_id):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(text="✔️ Tasdiqlash", callback_data=f'checked_{user_id}')
    )

    markup.add(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f'unchecked_{user_id}')
    )

    return markup
