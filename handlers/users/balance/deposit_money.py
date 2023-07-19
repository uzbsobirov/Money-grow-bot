import logging

from data.config import ADMINS
from loader import dp, bot
from states.balance import Balance
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

    text = f"<b>📤 To'lov turi</b>: <u>UZCARD</u>\n\n💳 <b>Karta</b>: <code>8600 0103 6666 7777</code>\n" \
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

        await state.finish()

    except Exception as error:
        logging.info(error)



