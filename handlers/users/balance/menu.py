from loader import dp, bot, db
from states.balance import Balance
from keyboards.inline.balance.menu import menues

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="💰 Hisobim", state='*')
async def check_user_balance(message: types.Message, state: FSMContext):
    get_bot = await bot.get_me()
    bot_username = get_bot.username
    user_id = message.from_user.id

    select_user = await db.select_user_data(user_id=user_id)
    print(select_user)
    balance = select_user[0][2]
    count = select_user[0][6]
    parent_id = select_user[0][5]

    photo = "https://t.me/almaz_medias/3"
    text = "<b>┌🏛 Sizning botdagi kabinetingiz\n" \
           "├\n├Botdagi vazifa: Foydalanuvchi\n" \
           f"├ID raqamingiz: {user_id}\n" \
           f"├Asosiy balans: {balance} so'm\n├Depozitingiz: 0 so'm\n" \
           f"├Sizni taklif qildi: {parent_id}\n├\n└@{bot_username} - Yuqori daromad!</b>"

    await message.answer_photo(photo=photo, caption=text, reply_markup=menues)

    await Balance.balance.set()