from loader import dp, bot
from keyboards.default.start import start_admin

from aiogram import types
from aiogram.dispatcher import FSMContext

from states.panel import Panel


@dp.callback_query_handler(text_contains="answer_to_", state='*')
async def answer_to_user_func(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    splited = data.split('_')
    user_id = splited[2]

    text = "Javobingizni yuboring..."
    await call.message.edit_text(
        text=text
    )

    await state.update_data(
        {'answer_user_id': user_id}
    )

    await Panel.answer_to_user.set()


@dp.message_handler(state=Panel.answer_to_user)
async def get_admin_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('answer_user_id')
    print(user_id)

    await message.send_copy(
        chat_id=user_id
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text="Javobingiz yuborildi",
        reply_markup=start_admin
    )

    await state.finish()
