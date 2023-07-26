from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db, bot
from utils.misc.checking import check_is_subs
from handlers.detectors import detect_is_admin
from keyboards.inline.check import check


@dp.callback_query_handler(text="check_subs", state='*')
async def check_func(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    bot_get_me = await bot.get_me()
    bot_username = bot_get_me.username

    data = await state.get_data()
    args = data.get('args')

    all_sponsors = await db.select_all_sponsor()

    un_subscribed = types.InlineKeyboardMarkup(row_width=1)

    await call.answer("Obuna tekshirilmoqda...")
    sub_status = 0

    for item in all_sponsors:
        check_user = await check_is_subs(user_id=user_id, chat_id=item[1])
        if check_user:
            pass

        else:
            sub_status += 1
            un_subscribed.insert(types.InlineKeyboardButton(text='❌ {}'.format(item[2]), url=item[4]))

    un_subscribed.add(types.InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))

    if sub_status != 0:
        text = "<b>❌Siz ba'zi kanallardan chiqib ketgansiz</b>"
        await call.message.edit_text(text=text, reply_markup=un_subscribed)

    else:
        await call.message.delete()
        photo = "https://t.me/almaz_medias/2"
        text = "👤 Assalomu alaykum, hurmatli mijoz!\n" \
               "📝 Botimiz qoidalari:\n├─Balansni to'ldiring\n" \
               "├─Investitsiya kiriting\n└─Pulni hisobingizga yechib oling\n\n" \
               "🔸 Ushbu loyiha sarmoyali daromad hisoblanib, to'lovlar uchun pul " \
               "foydalanuvchilarni sarmoyasidan va homiylardan olinadi!\n\n" \
               f"💬 Rasmiy guruh: @{bot_username}\n📢 Yangiliklar kanali: @{bot_username}"
        await call.message.answer_photo(photo=photo, caption=text, reply_markup=await detect_is_admin(user_id=user_id))



