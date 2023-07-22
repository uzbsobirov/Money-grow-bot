import logging

from handlers.detectors import detect_is_admin
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
               "<i>Mavjud to'lov turlari</i>\n▪️Qiwi\n▪️TRC 20\n▪️Payeer</b>"

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

    await Balance.money.set()


@dp.message_handler(state=Balance.money, content_types=types.ContentType.TEXT)
async def identify_how_much_money(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    msg = message.text

    select_user = await db.select_user_data(user_id)
    balance = select_user[0][1]

    try:
        summa = int(msg)
        if summa >= 10000:
            if balance >= summa:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="✅ Pul yechish uchun so'rovingiz qabul qilindi, admin tez orada to'lovni amalga oshiradi",
                    reply_markup=await detect_is_admin(user_id)
                )

                # await

                await state.update_data(
                    {'withdraw_user_id': user_id, 'how_much_money': summa}
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



