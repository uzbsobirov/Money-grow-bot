from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def check(sponsors, status):
    markup = InlineKeyboardMarkup(row_width=1)

    for item in sponsors:
        if status:
            pass
        else:
            markup.insert(
                InlineKeyboardButton(
                    text=item[2], url=item[4]
                )
            )
    markup.add(
        InlineKeyboardButton(
            text="✅ Tekshirish", callback_data='check_subs'
        )
    )
    return markup