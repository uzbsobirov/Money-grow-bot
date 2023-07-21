from datetime import datetime, date, timedelta

from loader import dp, db, bot
from keyboards.default.back import back

from aiogram import types
from aiogram.dispatcher import FSMContext

from states.panel import Panel


@dp.message_handler(text="📊 Statistika", state=Panel.menu)
async def admin_menu_statics(message: types.Message, state: FSMContext):
    get_me = await bot.get_me()
    bot_username = get_me.username

    todays_date = date.today()  # Todays date
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    all_users = await db.select_all_users()

    text = "<b>📅 Bugungi sana: {}\n" \
           "🕰 Hozirgi vaqt: {}\n\n" \
           "📊 Bot obunachilari soni: {}\n\n" \
           "⚡️ @{}</b>".format(todays_date, current_time, len(all_users), bot_username)

    await message.answer(text=text, reply_markup=back)
    await Panel.statistic.set()
