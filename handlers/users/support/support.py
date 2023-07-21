from keyboards.inline.admin.support import answer_to_user
from loader import dp, bot
from data.config import ADMINS
from keyboards.default.back import back
from handlers.detectors import detect_is_admin

from states.support import Support

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="📝 Murojaat", state='*')
async def support_to_admin(message: types.Message, state: FSMContext):
    text = "Savolingiz yoki taklifingiz bo'lsa yozib qoldiring✍️"
    await message.answer(text, reply_markup=back)

    await Support.text.set()


@dp.message_handler(state=Support.text, content_types=types.ContentType.ANY)
async def get_support_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    await message.answer(
        text="So'rovingiz adminga yuborildi, admin uni ko'rib chiqgandan keyin sizga javob beradi",
        reply_markup=await detect_is_admin(user_id)
    )

    await message.send_copy(chat_id=ADMINS[0], reply_markup=answer_to_user(user_id))

    await state.update_data(
        {'answer_user_id': user_id}
    )

    await state.reset_state(with_data=False)