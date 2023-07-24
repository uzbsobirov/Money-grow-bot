from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext

from states.balance import Balance


@dp.callback_query_handler(text="check_id", state=Balance.menu)
async def give_id_to_user(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id

    await call.message.answer(text=f'Sizning id: <code>{user_id}</code>')
