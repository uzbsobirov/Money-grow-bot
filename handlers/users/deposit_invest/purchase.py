from loader import dp, db
from states.invest import Invest
from handlers.detectors import detect_user_balance

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text_contains="purchase_", state=Invest.buy)
async def buy_some_type(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    data = call.data
    splited = data.split('_')
    user_datas = await db.select_user_data(user_id=user_id)
    balance = user_datas[0][2]

    check_user_afford = detect_user_balance(splited[1], balance)

    if check_user_afford is True:
        pass

    else:
        await call.answer(check_user_afford, show_alert=True)
