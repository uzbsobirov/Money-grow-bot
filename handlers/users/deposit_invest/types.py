from keyboards.inline.buy import purchase
from loader import dp
from keyboards.inline.invest.types import invest_types
from states.invest import Invest
from handlers.detectors import detect_type_name

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="➕ Investitsiya kiritish", state='*')
async def invest_types_func(message: types.Message, state: FSMContext):
    text = "<b>⬇️ Quyidagi tarflardan birini tanlang:</b>"

    await message.answer(text=text, reply_markup=invest_types)

    await Invest.types.set()


@dp.callback_query_handler(text_contains='tarif_', state=Invest.types)
async def get_invest_types(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    splited = data.split('_')
    type = detect_type_name(splited[1])

    text = f"<b>💰 Tarif nomi</b>: {type[0]}\n\n" \
           f"<b>▫️ Sarmoya narxi:</b> {type[1]} so'm\n" \
           f"▫<b>️ Jami daromad:</b> {type[2]} so'm\n" \
           f"<b>▫️ Kunlik daromad:</b> {type[3]} so'm\n\n" \
           f"Sarmoya kiritsangiz {type[4]} kun davomida kunlik {type[3]} so'm hisobingizga qo'shilib boradi!"

    await call.message.edit_text(text, reply_markup=purchase(data=splited[1]))

    await Invest.buy.set()