from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


informations = InlineKeyboardMarkup(row_width=2)
informations.add(
    InlineKeyboardButton(
        text="🥇 Investorlar (TOP)", callback_data='top_investors'
    )
)

informations.add(
    InlineKeyboardButton(
        text="💳 To'lovlar", url='t.me/kayzenuz'
    )
)
informations.insert(
    InlineKeyboardButton(
        text="💭 Muhokama", url='t.me/kayzenuz'
    )
)

informations.add(
    InlineKeyboardButton(
        text="☎️ Adminstrator", callback_data='support'
    )
)