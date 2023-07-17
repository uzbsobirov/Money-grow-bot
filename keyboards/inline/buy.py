from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def purchase(data):
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text="Sotib olish", callback_data=f'purchase_{data}'
        )
    )
    markup.add(
        InlineKeyboardButton(
            text="◀️ Orqaga", callback_data='back'
        )
    )

    return markup
