from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


informations = InlineKeyboardMarkup(row_width=2)
informations.add(
    InlineKeyboardButton(
        text="💳 To'lovlar", url='https://t.me/money_grow_tolovlar'
    )
)
informations.insert(
    InlineKeyboardButton(
        text="💭 Muhokama", url='https://t.me/money_grow_group'
    )
)

informations.add(
    InlineKeyboardButton(
        text="☎️ Adminstrator", callback_data='support'
    )
)