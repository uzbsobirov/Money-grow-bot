from handlers.detectors import detect_is_admin
from keyboards.inline.invest.types import invest_types
from loader import dp, bot, db
from keyboards.default.panel.menu import menues
from keyboards.inline.balance.menu import menues as balans_menu, payment_time
from states.balance import Balance

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

    photo = "https://t.me/almaz_medias/2"
    text = f"👤 Assalomu alaykum, hurmatli {full_name}!\n" \
           "📝 Botimiz qoidalari:\n▪️Balansni to'ldiring\n" \
           "▪️Investitsiya kiriting\n▪️Pulni hisobingizga yechib oling\n\n" \
           "🔸 Ushbu loyiha sarmoyali daromad hisoblanib, to'lovlar uchun pul " \
           "foydalanuvchilarni sarmoyasidan va homiylardan olinadi!\n\n" \
           f"💬 Rasmiy guruh: @{bot_username}\n📢 Yangiliklar kanali: @{bot_username}"
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
    get_bot = await bot.get_me()
    bot_username = get_bot.username
    user_id = call.from_user.id

    link = await get_start_link(user_id)

    await call.message.delete()

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
