from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    InlineKeyboardButton(text="📤 Pul kiritish", callback_data='deposit_money'),
    InlineKeyboardButton(text="📥 Pul yechish", callback_data='withdraw_money'),
    InlineKeyboardButton(text="🆔 Tekshirish", callback_data='check_id'),
    InlineKeyboardButton(text="🔄 O'tkazma", callback_data='transfer_money'),
]

menues = InlineKeyboardMarkup(row_width=2)
menues.add(*buttons)


def payment_time():
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="✅ To'lov qildim", callback_data='success_payment'
        )
    )

    markup.add(
        InlineKeyboardButton(
            text="◀️ Orqaga", callback_data='back'
        )
    )

    return markup


