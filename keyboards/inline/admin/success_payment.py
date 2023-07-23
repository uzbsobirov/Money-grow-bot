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


def withdraw_money_balance(user_id, summa):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text="✅ To'landi", callback_data=f'tolandi_{user_id}_{summa}')
    )

    markup.add(
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f'bekor_qilish_{user_id}_{summa}')
    )

    return markup
