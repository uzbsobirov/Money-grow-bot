from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


informations = InlineKeyboardMarkup(row_width=2)
informations.add(
    InlineKeyboardButton(
        text="💳 To'lovlar", url='https://t.me/alpha_tolovlar_kanali'
    )
)
informations.insert(
    InlineKeyboardButton(
        text="💭 Muhokama", url='https://t.me/ALPHA_group_uz'
    )
)

informations.add(
    InlineKeyboardButton(
        text="☎️ Adminstrator", callback_data='support'
    )
)