from loader import dp, bot, db
from keyboards.inline.data import informations

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link


@dp.message_handler(text="💵 Pul ishlash", state='*')
async def give_information(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    link = await get_start_link(user_id)

    photo_id = "https://t.me/almaz_medias/6"
    text = f"🔗 Sizning taklif xavolangiz:\n\n<code>{link}</code>\n\n" \
           "Kamida 4 ta aktiv investor taklif qilganingizdan soʻng sizga haftalik maosh olish imkoniyati ochiladi"

    await message.answer_photo(photo=photo_id, caption=text)

    await state.finish()

