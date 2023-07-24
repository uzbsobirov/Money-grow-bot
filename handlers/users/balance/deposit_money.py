import logging

from data.config import ADMINS
from loader import dp, bot, db
from states.balance import Balance, Payment
from keyboards.inline.balance.menu import payment_time
from keyboards.default.back import back
from handlers.detectors import detect_is_admin
from keyboards.inline.admin.success_payment import admin_check_payment

from aiogram.dispatcher import FSMContext
from aiogram import types


@dp.callback_query_handler(text="deposit_money", state=Balance.menu)
async def dposit_money_to_balance(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    user_mention = call.from_user.get_mention(full_name)

    await call.message.delete()

    text = f"📤 Xoxlagan to'lov turini tanlang va pul tashlang\n\n🟠 <b>Qiwi</b>: <code>+79804241329</code>\n" \
           f"🔵 <b>Payeer</b>: <code>P1096807701</code>\n" \
           f"🔘 <b>TRC 20</b>: <code>TG3JKEJahMHeHPWNEDLrSPaRqCEuTGtKPB</code>\n" \
           f"📝 <b>Izoh</b>: <code>{user_id}</code>\n\n" \
           f"📋 <b>Malumot:</b> <i>Tepadagi kartaga to'lov qiling, to'lov izohiga id " \
           f"raqamingizni qoldiring hamda to'lovingiz chekini ham saqlab qo'ying. " \
           f"So'ng <b>✅ To\'lov qildim</b> tugmasini bosib ma'lumotlarni yuboring</i>"

    await call.message.answer(text=text, reply_markup=payment_time())

    await state.update_data(
        {'user_id': user_id, 'user_mention': user_mention}
    )

    await Balance.deposit.set()


@dp.callback_query_handler(text="success_payment", state=Balance.deposit)
async def check_user_payment(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    text = "<b>To'lov chekini rasmini yuboring:</b>"

    await call.message.answer(text=text, reply_markup=back)

    await Balance.checkout.set()


@dp.message_handler(state=Balance.checkout, content_types=types.ContentType.ANY)
async def get_payment_check(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    user_mention = data.get('user_mention')

    try:
        photo_file_id = message.photo[-1].file_id
        text = "❇️ <b>Hisobni to'ldirganingiz haqida ma'lumot " \
               "asosiy adminga yuborildi. <u>Agar to'lovni amalga " \
               "oshirganingiz haqida ma'lumot mavjud bo'lsa</u>, hisobingiz to'ldiriladi.</b>"
        caption = f"👤 {user_mention}\n🆔 {user_id}"

        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=await detect_is_admin(user_id))

        await bot.send_photo(chat_id=ADMINS[0], photo=photo_file_id, caption=caption,
                                               reply_markup=admin_check_payment(user_id))

        await state.reset_state(with_data=False)

    except Exception as error:
        logging.info(error)


@dp.callback_query_handler(text_contains="checked_", state='*')
async def user_id_paid(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    splited = data.split('_')
    state_data = await state.get_data()

    if splited[0] == 'checked':
        await state.update_data(
            {'checked_user_id': splited[1]}
        )

        await call.message.delete()

        text = "<b>Foydalanuvchi balansini nech pul bilan to'ldirmoqchisiz?\n\nMasalan: <code>30000</code></b>"
        await call.message.answer(text, reply_markup=types.ReplyKeyboardRemove())

        await Payment.payment_time.set()

    elif splited[0] == 'unchecked':
        text = f"<b>⚠️ Hisobingizni to'ldirish bo'yicha yuborgan so'rovingiz qabul qilinmadi!</b>"
        await bot.send_message(chat_id=splited[1], text=text, reply_markup=await detect_is_admin(user_id=splited[1]))

        await call.message.delete()

        await bot.send_message(chat_id=call.message.chat.id, text="Hisob to'ldirish bekor qilindi",
                               reply_markup=await detect_is_admin(splited[1]))
        await state.finish()


@dp.message_handler(state=Payment.payment_time)
async def payment_touser(message: types.Message, state: FSMContext):
    msg = message.text
    data = await state.get_data()
    user_id = data.get('checked_user_id')

    try:
        summa = int(msg)

        select_user = await db.select_user_data(int(user_id))
        deposit = select_user[0][7]
        balance = select_user[0][2]

        real_balance = balance + summa
        real_deposit = deposit + summa

        await db.update_user_balance(balance=real_balance, deposit=real_deposit, user_id=int(user_id))

        text = f"<b>Hisobingizni {summa} Soʻm💸ga to'ldirish bo'yicha " \
               f"yuborgan so'rovingiz qabul qilindi va balansizga tushirildi!</b>"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=await detect_is_admin(user_id))

        await bot.send_message(chat_id=message.chat.id, text=f"Foydalanuvchi balansi {summa} so'm bilan to'ldirildi",
                               reply_markup=await detect_is_admin(user_id))

        await state.finish()

    except Exception as error:
        logging.info(error)
        await message.answer(text="Iltimos, faqat raqamlardan foydalaning")
