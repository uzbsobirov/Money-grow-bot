from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def answer_to_user(user_id):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(text="✔️ Javob berish", callback_data=f'answer_to_{user_id}')
    )

    return markup
