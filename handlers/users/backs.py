from handlers.detectors import detect_is_admin
from keyboards.inline.invest.types import invest_types
from loader import dp, bot

from states.invest import Invest

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text='back', state=Invest.types)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    username = call.from_user.username
    bot_get_me = await bot.get_me()
    bot_username = bot_get_me.username

    await call.message.delete()

    photo = "https://t.me/almaz_medias/2"
    text = f"👤 Assalomu alaykum, hurmatli {full_name}!\n" \
           "📝 Botimiz qoidalari:\n▪️Balansni to'ldiring\n" \
           "▪️Investitsiya kiriting\n▪️Pulni hisobingizga yechib oling\n\n" \
           "🔸 Ushbu loyiha sarmoyali daromad hisoblanib, to'lovlar uchun pul " \
           "foydalanuvchilarni sarmoyasidan va homiylardan olinadi!\n\n" \
           f"💬 Rasmiy guruh: @{bot_username}\n📢 Yangiliklar kanali: @{bot_username}"
    await call.message.answer_photo(photo=photo, caption=text, reply_markup=await detect_is_admin(user_id=user_id))

    await state.finish()


@dp.callback_query_handler(text='back', state=Invest.buy)
async def move_to_main_menu(call: types.CallbackQuery, state: FSMContext):
    text = "<b>⬇️ Quyidagi tarflardan birini tanlang:</b>"

    await call.message.edit_text(text=text, reply_markup=invest_types)

    await Invest.types.set()
