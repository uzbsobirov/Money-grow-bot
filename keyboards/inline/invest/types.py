from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


invest_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Vip 1", callback_data='tarif_one'
            ),
            InlineKeyboardButton(
                text="Vip 2", callback_data='tarif_two'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Vip 3", callback_data='tarif_three'
            ),
            InlineKeyboardButton(
                text="Vip 4", callback_data='tarif_four'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Vip 5", callback_data='tarif_five'
            ),
            InlineKeyboardButton(
                text="Vip 6", callback_data='tarif_six'
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga", callback_data='back'
            )
        ]
    ]
)