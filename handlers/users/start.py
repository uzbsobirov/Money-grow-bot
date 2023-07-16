from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot
from handlers.detectors import detect_is_admin
from utils.misc.checking import check_is_subs
from keyboards.inline.check import check

from datetime import datetime

today = datetime.today()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    full_name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id
    user_mention = message.from_user.get_mention(name=full_name, as_html=True)
    bot_get_me = await bot.get_me()
    bot_username = bot_get_me.username

    # Add the User to the DB
    try:
        await db.add_user(
            full_name=full_name,
            username=username,
            user_id=user_id,
            join_date=today
        )

        # About message to ADMIN
        msg = f"{user_mention} [<code>{user_id}</code>] bazaga qo'shildi."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except:
        await bot.send_message(chat_id=ADMINS[0],
                               text=f"{user_mention} [<code>{user_id}</code>] bazaga oldin qo'shilgan")

    all_sponsors = await db.select_all_sponsor()

    if len(all_sponsors) == 0:
        photo = "https://t.me/almaz_medias/2"
        text = f"👤 Assalomu alaykum, hurmatli {full_name}!\n" \
               "📝 Botimiz qoidalari:\n▪️Balansni to'ldiring\n" \
               "▪️Investitsiya kiriting\n▪️Pulni hisobingizga yechib oling\n\n" \
               "🔸 Ushbu loyiha sarmoyali daromad hisoblanib, to'lovlar uchun pul " \
               "foydalanuvchilarni sarmoyasidan va homiylardan olinadi!\n\n" \
               f"💬 Rasmiy guruh: @{bot_username}\n📢 Yangiliklar kanali: @{bot_username}"
        await message.answer_photo(photo=photo, caption=text, reply_markup=await detect_is_admin(user_id=user_id))
    else:
        sub_status = False
        for item in all_sponsors:
            check_user = await check_is_subs(user_id=user_id, chat_id=item[1])
            if check_user:
                sub_status = True
            else:
                pass

        if not sub_status:
            text = "You have to subscribe to the channels and groups"
            await message.answer(text=text, reply_markup=check(sponsors=all_sponsors, status=sub_status))

        else:
            photo = "https://t.me/almaz_medias/2"
            text = "👤 Assalomu alaykum, hurmatli mijoz!\n" \
                   "📝 Botimiz qoidalari:\n├─Balansni to'ldiring\n" \
                   "├─Investitsiya kiriting\n└─Pulni hisobingizga yechib oling\n\n" \
                   "🔸 Ushbu loyiha sarmoyali daromad hisoblanib, to'lovlar uchun pul " \
                   "foydalanuvchilarni sarmoyasidan va homiylardan olinadi!\n\n" \
                   f"💬 Rasmiy guruh: @{bot_username}\n📢 Yangiliklar kanali: @{bot_username}"
            await message.answer_photo(photo=photo, caption=text, reply_markup=await detect_is_admin(user_id=user_id))
