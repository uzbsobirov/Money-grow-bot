from handlers.detectors import detect_type_name
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
    full_name = message.from_user.full_name

    link = await get_start_link(user_id)

    active = 0
    nonactive = 0
    select_user_teams = await db.select_one_user_team(user_id)

    for user in select_user_teams:
        if user[3] is not None:
            active += 1

        else:
            nonactive += 1

    select_user = await db.select_user_data(user_id=user_id)
    balance = select_user[0][2]
    date_joined = select_user[0][-1]
    status = select_user[0][3]
    bonus_money = select_user[0][10]

    detect_status = detect_type_name(status)

    photo = "https://t.me/almaz_medias/10"
    if len(detect_status) != 0:
        text = "Hisobingiz ma'lumotlari!\n\n" \
               f"Foydalanuvchi identifikatori🛠️: {user_id}\n" \
               f"Sizning VIP⚙️: {detect_status[0]}\n" \
               f"Sizning pulingiz💰: {balance} \n" \
               f"Keshbekingiz🪙: {bonus_money} so'm\n" \
               f"Do'stlaringiz👬: {active}\n" \
               f"Ismingiz📡: {full_name}\n\n" \
               f"Siz bizning platformamizdan buyon foydalanasiz - {date_joined}"

        await message.answer_photo(photo=photo, caption=text, reply_markup=menues)

    else:
        print('if 1-1')
        text = "Hisobingiz ma'lumotlari!\n\n" \
               f"Foydalanuvchi identifikatori🛠️: {user_id}\n" \
               f"Sizning VIP⚙️: {detect_status[0]}\n" \
               f"Sizning pulingiz💰: {balance} \n" \
               f"Keshbekingiz🪙: {bonus_money} so'm\n" \
               f"Do'stlaringiz👬: {active}\n" \
               f"Ismingiz📡: {full_name}\n\n" \
               f"Siz bizning platformamizdan buyon foydalanasiz - {date_joined}"

        await message.answer_photo(photo=photo, caption=text, reply_markup=menues)

    await Balance.menu.set()
