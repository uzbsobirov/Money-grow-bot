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
           f"✅Har bir taklif qilgan faol doʻstingiz uchun har kuni 1500 soʻm maosh olasiz.\n" \
           f"✅Jamoa sardorlari faol jamoasi 10 kishiga yetganda 100000 soʻm mukofot bilan taqdirlanadilar❗️❗️"

    await message.answer_photo(photo=photo_id, caption=text)

    await state.finish()

