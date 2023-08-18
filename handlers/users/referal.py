from loader import dp, bot, db
from keyboards.inline.data import informations

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link


@dp.message_handler(text="🔗 Referal", state='*')
async def give_information(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    link = await get_start_link(user_id)

    photo_id = "https://t.me/almaz_medias/11"
    text = "🔗 Sizning taklif xavolangiz:\n\n" \
           f"<code>{link}</code>\n\n" \
           "👥Har bir botga investetsiya kiritgan hamkoringizdan 15 % ulush olasiz"

    await message.answer_photo(photo=photo_id, caption=text)

    await state.finish()

