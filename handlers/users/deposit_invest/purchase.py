import pytz
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp, db, bot
from states.invest import Invest
from handlers.detectors import detect_user_balance, detect_type_name, detect_is_admin

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import executor

from . import daily_bonus

tz = pytz.timezone('Asia/Tashkent')

scheduler = AsyncIOScheduler(
    timezone=tz
)


@dp.callback_query_handler(text_contains="purchase_", state=Invest.buy)
async def buy_some_type(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    data = call.data
    splited = data.split('_')
    user_data = await db.select_user_data(user_id=user_id)
    balance = user_data[0][2]

    check_user_afford = detect_user_balance(splited[1], balance)

    detect_type = detect_type_name(data=splited[1])

    if user_data[0][3] is None:
        if check_user_afford is True:
            await call.message.delete()

            await call.message.answer(
                text=f"🎉 Tabriklaymiz, siz {detect_type[0]} tarifini sotib oldingiz",
                reply_markup=await detect_is_admin(user_id)
            )

            new_balance = balance - detect_type[1]
            await db.update_user_balancee(balance=new_balance, user_id=user_id)

            await db.update_user_invest(type_invest=splited[1], end_invest_date=35, user_id=user_id)

            if user_data[0][4] < 36:
                scheduler.add_job(daily_bonus.job, trigger='interval', minutes=1,
                                  kwargs={'user_id': user_id, 'tarif': detect_type[3], 'call': call, 'bot': bot})

            # if user_data[0][4] == 0:
            #     print(2)
            #     await db.update_user_invest(type_invest=None, end_invest_date=0, user_id=user_id)

            await state.finish()
        else:
            await call.answer(check_user_afford, show_alert=True)

    else:
        await call.answer(text=f"Siz allaqachon {detect_type[0]} tarifni tanlagansiz", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
