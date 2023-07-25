from loader import dp, bot, db
from states.balance import Balance
from keyboards.inline.balance.menu import menues

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link


@dp.message_handler(text="💰 Hisobim", state='*')
async def check_user_balance(message: types.Message, state: FSMContext):
    get_bot = await bot.get_me()
    bot_username = get_bot.username
    user_id = message.from_user.id

    link = await get_start_link(user_id)

    cnt = 0
    select_user_teams = await db.select_one_user_team(user_id)

    for user in select_user_teams:
        if user[3] is not None:
            cnt += 1

    select_user = await db.select_user_data(user_id=user_id)
    balance = select_user[0][2]
    deposit = select_user[0][7]

    photo = "https://t.me/almaz_medias/3"
    text = "<b>┌🏛 Sizning botdagi kabinetingiz\n" \
           f"├Link: <code>{link}</code>\n├Botdagi vazifa: Foydalanuvchi\n" \
           f"├ID raqamingiz: {user_id}\n" \
           f"├Asosiy balans: {balance} so'm\n├Depozitingiz: {deposit} so'm\n" \
           f"├Siz taklif qilganlar soni: {cnt}\n├\n└@{bot_username} - Yuqori daromad!</b>"

    await message.answer_photo(photo=photo, caption=text, reply_markup=menues)

    await Balance.menu.set()