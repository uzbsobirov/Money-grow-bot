from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


invest_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Vib 1", callback_data='tarif_one'
            ),
            InlineKeyboardButton(
                text="Vib 2", callback_data='tarif_two'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Vib 3", callback_data='tarif_three'
            ),
            InlineKeyboardButton(
                text="Vib 4", callback_data='tarif_four'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Vib 5", callback_data='tarif_five'
            ),
            InlineKeyboardButton(
                text="Vib 6", callback_data='tarif_six'
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga", callback_data='back'
            )
        ]
    ]
)