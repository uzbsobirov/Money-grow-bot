from handlers.detectors import detect_is_admin, detect_type_name
from keyboards.inline.data import informations
from keyboards.inline.invest.types import invest_types
from loader import dp, bot, db
from keyboards.default.panel.menu import menues
from keyboards.inline.balance.menu import menues
from keyboards.inline.balance.menu import menues as balans_menu, payment_time
from states.balance import Balance
from keyboards.default.back import back
from states.data import Data

from states.invest import Invest
from states.panel import Panel
from states.support import Support

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link


@dp.callback_query_handler(text='back', state=Invest.types)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    bot_get_me = await bot.get_me()
    bot_username = bot_get_me.username

    await call.message.delete()

    photo = "https://t.me/almaz_medias/12"
    text = "🇺🇿 Assalomu alaykum, hurmatli mijoz!\n" \
           "📝 Botimiz qoidalari:\n" \
           "▪️ Balansni to'ldiring\n" \
           "▪️ Investitsiya kiriting\n" \
           "▪️ Pulni hisobingizga yechib oling\n\n" \
           "💹 MONIY GROW - ga xush kelibsiz, bu yerda siz edial daromad olishingiz mumkun.\n" \
           "Botning imkoniyatlari tez toʻlov va ishonchli sarmoya \n\n" \
           "💬 Rasmiy guruh: @money_grow_group\n📢 To'lovlar kanali: @money_grow_tolovlar"
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await detect_is_admin(user_id=user_id))

    await state.finish()


@dp.callback_query_handler(text='back', state=Invest.buy)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    text = "<b>⬇️ Quyidagi tarflardan birini tanlang:</b>"

    await call.message.edit_text(text=text, reply_markup=invest_types)

    await Invest.types.set()


@dp.message_handler(text="◀️ Orqaga", state=Panel.statistic)
async def move_to_admin_menu(message: types.Message, state: FSMContext):
    text = "🖥 Admin menu"
    await message.answer(text=text, reply_markup=menues)

    await Panel.menu.set()


@dp.message_handler(text="◀️ Orqaga", state=Panel.sponsor)
async def move_to_admin_menu(message: types.Message, state: FSMContext):
    text = "🖥 Admin menu"
    await message.answer(text=text, reply_markup=menues)

    await Panel.menu.set()


@dp.message_handler(text="◀️ Orqaga", state=Panel.menu)
async def move_to_admin_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    text = "🖥 Asosiy menu"
    await message.answer(text=text, reply_markup=await detect_is_admin(user_id))

    await state.finish()


@dp.message_handler(text="◀️ Orqaga", state=Support.text)
async def move_to_admin_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    text = "🖥 Asosiy menu"
    await message.answer(text=text, reply_markup=await detect_is_admin(user_id))

    await state.finish()


@dp.callback_query_handler(text='back', state=Balance.deposit)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    full_name = call.from_user.full_name
    user_id = call.from_user.id

    await call.message.delete()

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

        await call.message.answer_photo(photo=photo, caption=text, reply_markup=balans_menu)

    else:
        text = "Hisobingiz ma'lumotlari!\n\n" \
               f"Foydalanuvchi identifikatori🛠️: {user_id}\n" \
               f"Sizning VIP⚙️: {detect_status[0]}\n" \
               f"Sizning pulingiz💰: {balance} \n" \
               f"Keshbekingiz🪙: {bonus_money} so'm\n" \
               f"Do'stlaringiz👬: {active}\n" \
               f"Ismingiz📡: {full_name}\n\n" \
               f"Siz bizning platformamizdan buyon foydalanasiz - {date_joined}"

        await call.message.answer_photo(photo=photo, caption=text, reply_markup=balans_menu)

    await Balance.menu.set()


@dp.message_handler(text="◀️ Orqaga", state=Balance.checkout)
async def move_to_admin_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_mention = message.from_user.get_mention(full_name)

    await message.delete()

    text = f"<b>📤 To'lov turi</b>: <u>UZCARD</u>\n\n💳 <b>Karta</b>: <code>8600 0103 6666 7777</code>\n" \
           f"📝 <b>Izoh</b>: <code>{user_id}</code>\n\n" \
           f"📋 <b>Malumot:</b> <i>Tepadagi kartaga to'lov qiling, to'lov izohiga id " \
           f"raqamingizni qoldiring hamda to'lovingiz chekini ham saqlab qo'ying. " \
           f"So'ng <b>✅ To\'lov qildim</b> tugmasini bosib ma'lumotlarni yuboring</i>"

    await message.answer(text=text, reply_markup=payment_time())

    await state.update_data(
        {'user_id': user_id, 'user_mention': user_mention}
    )

    await Balance.deposit.set()


@dp.message_handler(text='◀️ Orqaga', state=Balance.withdraw)
async def move_to_main_menu(message: types.Message, state: FSMContext):
    full_name = message.from_user.full_name
    user_id = message.from_user.id

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

        await message.answer_photo(photo=photo, caption=text, reply_markup=balans_menu)

    else:
        text = "Hisobingiz ma'lumotlari!\n\n" \
               f"Foydalanuvchi identifikatori🛠️: {user_id}\n" \
               f"Sizning VIP⚙️: {detect_status[0]}\n" \
               f"Sizning pulingiz💰: {balance} \n" \
               f"Keshbekingiz🪙: {bonus_money} so'm\n" \
               f"Do'stlaringiz👬: {active}\n" \
               f"Ismingiz📡: {full_name}\n\n" \
               f"Siz bizning platformamizdan buyon foydalanasiz - {date_joined}"

        await message.answer_photo(photo=photo, caption=text, reply_markup=balans_menu)

    await Balance.menu.set()


@dp.message_handler(text='◀️ Orqaga', state=Balance.money)
async def move_to_main_menu(message: types.Message, state: FSMContext):
    text = "<b>Pul yechib olish uchun karta raqami kiriting...\n\n" \
           "<i>Mavjud to'lov turlari</i>\n▪️Qiwi\n▪️TRC 20\n▪️Payeer</b>"

    await message.answer(text, reply_markup=back)

    await Balance.withdraw.set()


@dp.message_handler(text='◀️ Orqaga', state=Balance.cancel_payment)
async def move_to_main_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    text = "🖥 Asosiy menu"
    await message.answer(text=text, reply_markup=await detect_is_admin(user_id))

    await state.finish()


@dp.callback_query_handler(text='back', state=Data.investors)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
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

    await call.message.delete()
    await call.message.answer(text=text, reply_markup=informations)

    await Data.information.set()


@dp.message_handler(text='◀️ Orqaga', state=Panel.delete)
async def move_to_main_menu(message: types.Message, state: FSMContext):
    text = "🖥 Admin menu"
    await message.answer(text=text, reply_markup=menues)

    await Panel.menu.set()


@dp.message_handler(text='◀️ Orqaga', state=Balance.id)
async def move_to_main_menu(message: types.Message, state: FSMContext):
    get_bot = await bot.get_me()
    bot_username = get_bot.username
    user_id = message.from_user.id

    link = await get_start_link(user_id)

    select_user = await db.select_user_data(user_id=user_id)
    balance = select_user[0][2]
    deposit = select_user[0][7]
    parent_id = select_user[0][5]

    photo = "https://t.me/almaz_medias/3"
    text = "<b>┌🏛 Sizning botdagi kabinetingiz\n" \
           f"├Link: <code>{link}</code>\n├Botdagi vazifa: Foydalanuvchi\n" \
           f"├ID raqamingiz: {user_id}\n" \
           f"├Asosiy balans: {balance} so'm\n├Depozitingiz: {deposit} so'm\n" \
           f"├Sizni taklif qildi: {parent_id}\n├\n└@{bot_username} - Yuqori daromad!</b>"

    await message.answer_photo(photo=photo, caption=text, reply_markup=balans_menu)

    await Balance.menu.set()