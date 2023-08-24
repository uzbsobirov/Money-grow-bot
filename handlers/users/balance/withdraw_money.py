import logging

from handlers.detectors import detect_is_admin
from keyboards.default.start import start_admin
from keyboards.inline.admin.success_payment import withdraw_money_balance
from loader import dp, bot, db
from data.config import ADMINS
from keyboards.default.back import back

from states.balance import Balance

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="withdraw_money", state=Balance.menu)
async def withdraaw_money_from_balance(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    select_user = await db.select_user_data(user_id)
    balance = select_user[0][1]

    if balance >= 10000:
        text = "<b>Pul yechib olish uchun karta raqami kiriting...\n\n" \
               "<i>Mavjud to'lov turlari</i>\n\n▪️Humo</b>"

        await call.message.delete()
        await call.message.answer(text=text, reply_markup=back)

        await Balance.withdraw.set()

    else:
        text = "⚠️ Pul chiqarish uchun hisobingizda kamida 10.000 so'm bo'lishi shart!"
        await call.answer(text, show_alert=True)


@dp.message_handler(state=Balance.withdraw, content_types=types.ContentType.TEXT)
async def identify_card(message: types.Message, state: FSMContext):
    msg = message.text

    await message.answer(
        text="Yaxshi, endi nech pul chiqarib olmoqchi ekanligingizni yozing\n\nMasalan: <code>10000</code>",
        reply_markup=back
    )

    await state.update_data(
        {'card_number': msg}
    )

    await Balance.money.set()


@dp.message_handler(state=Balance.money, content_types=types.ContentType.TEXT)
async def identify_how_much_money(message: types.Message, state: FSMContext):
    data = await state.get_data()
    card_number = data.get('card_number')

    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_mention = message.from_user.get_mention(name=full_name)

    msg = message.text

    select_user = await db.select_user_data(user_id)
    balance = select_user[0][2]

    try:
        summa = int(msg)
        if summa >= 10000:
            if balance >= summa:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="✅ Pul yechish uchun so'rovingiz qabul qilindi, admin tez orada to'lovni amalga oshiradi",
                    reply_markup=await detect_is_admin(user_id)
                )

                admin_text = f"👤 {user_mention}\n💳 {card_number}\n💸 {summa} so'm\n💰 {balance}"

                await bot.send_message(
                    chat_id=ADMINS[0],
                    text=admin_text,
                    reply_markup=withdraw_money_balance(user_id, summa)
                )

                await state.reset_state(with_data=False)

            elif balance < summa:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Hisobingizda {balance} so'm pul va siz {summa} so'm "
                         f"chiqarishga harakat qilyapsiz, iltimos boshqattan urinib ko'ring\n\n"
                         f"Masalan: <code>10000</code>",
                    reply_markup=back
                )

        else:
            text = "⚠️ Eng kamida 10000 so'm chiqarib olish mumkin, summa kiriting\n\nMasalan: <code>10000</code>"
            await message.answer(text, reply_markup=back)

    except ValueError as VE:
        logging.info(VE)
        await message.answer(
            text='Iltimos, faqat raqamlardan foydalaning\n\nMasalan: <code>10000</code>',
            reply_markup=back
        )


@dp.callback_query_handler(text_contains="tolandi_", state='*')
async def final_withdraw(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    splited = data.split('_')

    user_id = splited[1]
    summa = splited[2]

    select_user_data = await db.select_user_data(int(user_id))
    balance = select_user_data[0][2]

    get_user = await bot.get_chat(user_id)
    full_name = get_user.full_name
    user_mention = call.from_user.get_mention(full_name)

    end_balance = balance - int(summa)
    await db.update_user_balancee(end_balance, int(user_id))

    await call.message.delete()

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Foydalanuvchi puli to'lab berildi",
        reply_markup=start_admin
    )

    text = f"✅ Pul toʻlandi: {user_mention}\n" \
           f"👤 Foydalanuvchi ID: {user_id}\n" \
           f"💸 Miqdor: {summa} soʻm"

    await bot.send_message(
        chat_id=-1001943689507,
        text=text
    )

    await bot.send_message(
        chat_id=user_id,
        text=f"Sizning pul yechish so'rovingiz qabul qilindi va {summa} so'm to'lab berildi",
        reply_markup=await detect_is_admin(user_id)
    )

    await state.finish()


@dp.callback_query_handler(text_contains="bekor_qilish_", state='*')
async def final_withdraw(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    splited = data.split('_')

    user_id = splited[2]
    summa = splited[3]

    await call.message.delete()

    await state.update_data(
        {'final_id': user_id, 'final_summa': summa}
    )

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="To'lov bekor bo'lishining sababini kiriting",
        reply_markup=back
    )

    await Balance.cancel_payment.set()


@dp.message_handler(state=Balance.cancel_payment, content_types=types.ContentType.TEXT)
async def cancel_payment_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('final_id')
    final_summa = data.get('final_summa')

    msg = message.text

    await bot.send_message(
        chat_id=user_id,
        text=f"Sizning {final_summa} so'm chiqarishdagi harakatingiz bekor qilindi\n\nSabab: {msg}"
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Xabar foydalanuvchiga yuborildi va to'lov harakati bekor qilindi",
        reply_markup=start_admin
    )

    await state.finish()