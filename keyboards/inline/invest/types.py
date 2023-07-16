from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


invest_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⚫️ Temir", callback_data='tarif_temir'
            ),
            InlineKeyboardButton(
                text="🟤 Bronza", callback_data='tarif_bronza'
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔘 Kumush", callback_data='tarif_kumush'
            ),
            InlineKeyboardButton(
                text="🟡 Oltin", callback_data='tarif_oltin'
            ),
        ],
        [
            InlineKeyboardButton(
                text="💎 Olmos", callback_data='tarif_olmos'
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga", callback_data='back'
            )
        ]
    ]
)