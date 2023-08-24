import pytz
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.detectors import detect_user_balance, detect_type_name, detect_is_admin
from loader import dp, db, bot
from states.invest import Invest
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
    parent_id = user_data[0][5]
    which_type = user_data[0][3]

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

            await db.update_user_invest(type_invest=splited[1], end_invest_date=30, user_id=user_id)

            if user_data[0][4] < 31:
                scheduler.add_job(daily_bonus.job, trigger='interval', seconds=1,
                                  kwargs={'user_id': user_id, 'tarif': detect_type[3], 'call': call,
                                          'scheduler': scheduler})

            detect_discount = (detect_type[1] * 15) / 100
            if parent_id:
                await db.update_user_bonus_id(bonus_id=1, user_id=parent_id)
                user_info = await db.select_user_data(user_id=user_id)
                bonus_id = user_info[0][9]

                select_parent_id = await db.select_user_data(user_id=parent_id)
                parent_balance = select_parent_id[0][2]
                bonus_money = select_parent_id[0][10]
                if bonus_id != 1:
                    await db.update_user_balancee(balance=parent_balance + int(detect_discount), user_id=parent_id)
                    await db.update_user_bonus_meney(bonus_money=bonus_money + int(detect_discount), user_id=parent_id)
                    await bot.send_message(
                        chat_id=parent_id,
                        text="Sizning hisobingizga bonus puli qo'shildi"
                    )

            await state.finish()
        else:
            await call.answer(check_user_afford, show_alert=True)

    else:
        await call.answer(text=f"Siz allaqachon {detect_type_name(which_type)[0]} tarifni tanlagansiz", show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
