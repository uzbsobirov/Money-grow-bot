from loader import dp, bot, db
from keyboards.inline.data import informations
from states.data import Data
from keyboards.inline.back import back

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="📚 Ma'lumot", state='*')
async def give_information(message: types.Message, state: FSMContext):
    get_bot = await bot.get_me()
    bot_username = get_bot.username

    all_user = await db.count_users()
    len_active_deposit = 0
    active_deposit = 0
    nonactive = 0

    select_users_data = await db.select_all_users_datas()

    for user_data in select_users_data:
        if user_data[3] is None:
            nonactive += 1

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

    photo_link = "https://t.me/almaz_medias/8"
    await message.answer_photo(photo=photo_link, caption=text, reply_markup=informations)

    await Data.information.set()


@dp.callback_query_handler(text="top_investors", state=Data.information)
async def give_top_investors(call: types.CallbackQuery, state: FSMContext):

    top_invest_user = await db.select_all_users_datas()

    lst_top_users = []

    for user in top_invest_user:
        if user[3] is not None:
            if len(lst_top_users) < 10:
                lst_top_users.append({'user_id': user[1], 'deposit': user[7]})

        else:
            pass

    lst_top_users.sort(key=lambda x: x['deposit'], reverse=True)

    text = f"🥇TOP 10 ta investorlar\n\n"
    cnt = 1
    for item in lst_top_users:
        get_data = await bot.get_chat(item['user_id'])

        text += f"{cnt}) <code>{get_data.full_name}</code>[<code>{item['user_id']}</code>] -- {item['deposit']} so'm\n"
        cnt += 1

    await call.message.edit_text(text, reply_markup=back)

    await Data.investors.set()

    lst_top_users.clear()


@dp.callback_query_handler(text="support", state=Data.information)
async def support_to_admin(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text="@ALPHA_admin8989"
    )

