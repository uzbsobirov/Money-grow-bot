import pytz
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from loader import dp, db
from states.invest import Invest
from handlers.detectors import detect_user_balance, detect_type_name, detect_is_admin

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import executor

tz = pytz.timezone('Asia/Tashkent')

scheduler = AsyncIOScheduler(
    timezone=tz
)


async def job():
    print('Hello world')


@dp.callback_query_handler(text_contains="purchase_", state=Invest.buy)
async def buy_some_type(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    data = call.data
    splited = data.split('_')
    user_datas = await db.select_user_data(user_id=user_id)
    balance = user_datas[0][2]

    check_user_afford = detect_user_balance(splited[1], balance)

    detect_type = detect_type_name(data=splited[1])

    if user_datas[0][3] is not None:
        if check_user_afford is True:
            await call.message.delete()

            await call.message.answer(
                text=f"🎉 Tabriklaymiz, siz {detect_type[0]} tarifini sotib oldingiz",
                reply_markup=await detect_is_admin(user_id)
            )

            await db.update_user_invest(type_invest=splited[1], end_invest_date=35, user_id=user_id)

            if user_datas[0][4] < 36:
                try:
                    scheduler.add_job(job, trigger='interval', minutes=1)
                    asyncio.get_event_loop().run_forever()
                    scheduler.start()
                except:
                    pass

                await db.update_user_end_invest(user_id)

            await state.finish()
        else:
            await call.answer(check_user_afford, show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
