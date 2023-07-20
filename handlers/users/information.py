from loader import dp, bot, db
from keyboards.inline.data import informations

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="📚 Ma'lumot", state='*')
async def give_information(message: types.Message, state: FSMContext):
    get_bot = await bot.get_me()
    bot_username = get_bot.username

    all_user = await db.count_users()
    len_active_deposit = 0
    active_deposit = 0

    select_users_data = await db.select_all_users_datas()

    for user_data in select_users_data:
        if user_data[3] is None:
            pass

        else:
            len_active_deposit += 1

    for user_data in select_users_data:
        if user_data[7] == 0:
            pass

        else:
            active_deposit += user_data[7]

    text = f"@{bot_username} - Loyiha statistikasi\n\n" \
           f"👥Aktiv foydalanuvchilar: {all_user} ta\n" \
           f"📈Aktiv sarmoyalar: {len_active_deposit} ta\n" \
           f"📥Kiritilgan pullar: {active_deposit} so'm"

    await message.answer(text=text, reply_markup=informations)


