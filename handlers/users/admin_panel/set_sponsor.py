import logging

from handlers.detectors import detect_is_admin
from keyboards.default.panel.sponsor import needed, have_needed
from keyboards.default.start import start_admin
from loader import dp, db, bot
from states.panel import Panel
from keyboards.inline.admin.add_sponsor import add_sponsor
from datetime import datetime
from keyboards.default.back import back
from keyboards.default.panel.sponsor import back as back_to_majburiy

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import Unauthorized, BadRequest

from utils.misc.checking import check_is_admin


@dp.message_handler(text="🔐 Majburiy obuna", state=Panel.menu)
async def set_sponsors(message: types.Message, state: FSMContext):
    all_sponsor = await db.select_all_sponsor()

    txt = "<b>Majburiy obuna ulanganlar👇</b>\n\n"
    count = 1

    if len(all_sponsor) == 0:
        text = "<b>Majburoy obuna ulanmagan🙅‍♂️</b>"
        await message.answer(text=text, reply_markup=add_sponsor)
    else:
        for item in all_sponsor:
            txt += f"{count}) <code>{item[1]}</code> | <a href='{item[4]}'>{item[2]}</a>\n"
            count += 1

        await message.answer(text=txt, reply_markup=have_needed, disable_web_page_preview=True)

    await Panel.sponsor.set()


@dp.callback_query_handler(text="add_sponsor", state=Panel.sponsor)
async def add_new_sponsor(call: types.CallbackQuery, state: FSMContext):
    text = "<b>Ulamoqchi bo'lgan kanalingizdan birorta postni <i>forward</i> qilib yuboring\n\n" \
           "⚠️ Bot ulamoqchi bo'lgan kanalingizda yoki guruhingizda admin bo'lishi shart❗️</b>"
    await call.message.edit_text(text=text)

    await Panel.get_data.set()


@dp.message_handler(state=Panel.get_data, content_types=types.ContentType.ANY)
async def get_sponsor_data(message: types.Message, state: FSMContext):
    data = await bot.get_me()
    bot_username = data.username

    chat_id = message.forward_from_chat.id
    chat_title = message.forward_from_chat.title
    chat_type = message.forward_from_chat.type

    get_channel_data = await bot.get_chat(chat_id=chat_id)

    time = datetime.now()

    try:
        checking = await check_is_admin(chat_id=chat_id)
        for item in checking:
            if item.user.username == bot_username and item.status == 'administrator':
                await message.answer(text="Kanal Majburiy obuna ro'yhatiga qo'shildi✅", reply_markup=start_admin)
                chat_link = await get_channel_data.export_invite_link()
                await db.add_sponsor(
                    chat_id=chat_id,
                    chat_title=chat_title,
                    chat_link=chat_link,
                    chat_type=chat_type,
                    join_date=time
                )
                await state.finish()
                break

    except (Unauthorized, BadRequest) as UB:
        logging.info(UB)
        text = "<b>Bot kanalda admin emas. Iltimos admin qilib keyin qaytadan urinib ko'ring❗️</b>"
        await message.answer(text=text, reply_markup=back)


@dp.message_handler(text="➕ Qo'shish", state=Panel.sponsor)
async def add_new_sponsor(message: types.Message, state: FSMContext):
    text = "<b>Ulamoqchi bo'lgan kanalingizdan birorta postni <i>forward</i> qilib yuboring\n\n" \
           "⚠️ Bot ulamoqchi bo'lgan kanalingizda yoki guruhingizda admin bo'lishi shart❗️</b>"
    await message.answer(text=text)

    await Panel.get_data.set()


@dp.message_handler(state=Panel.get_data, content_types=types.ContentType.ANY)
async def get_sponsor_data(message: types.Message, state: FSMContext):
    data = await bot.get_me()
    bot_username = data.username

    chat_id = message.forward_from_chat.id
    chat_title = message.forward_from_chat.title
    chat_type = message.forward_from_chat.type
    print(message)

    get_channel_data = await bot.get_chat(chat_id=chat_id)
    chat_link = await get_channel_data.export_invite_link()

    checking = await check_is_admin(chat_id=chat_id)

    time = datetime.now()

    for item in checking:
        if item.user.username == bot_username and item.status == 'administrator':
            await message.answer(text="Kanal Majburiy obuna ro'yhatiga qo'shildi✅", reply_markup=start_admin)
            await db.add_sponsor(
                chat_id=chat_id,
                chat_title=chat_title,
                chat_link=chat_link,
                chat_type=chat_type,
                date_joined=time
            )
            await state.finish()
            break
        else:
            text = "<b>Bot kanalda admin emas. Iltimos admin qilib keyin qaytadan urinib ko'ring❗️</b>"
            await message.answer(text=text, reply_markup=back)


@dp.message_handler(text="🗑 Kanalni o'chirish", state=Panel.sponsor)
async def delete_sponsor(message: types.Message, state: FSMContext):
    all_sponsor = await db.select_all_sponsor()

    txt = "<b>Majburiy obuna ulanganlar👇</b>\n\n"
    count = 1

    for item in all_sponsor:
        txt += f"{count}) <code>{item[1]}</code> | <a href='{item[4]}'>{item[2]}</a>\n"
        count += 1

    txt += "\n<b>Qaysi kanalni o'chirmoqchi bo'lsangiz id ni kiriting👇</b>"

    await message.answer(text=txt, reply_markup=back_to_majburiy, disable_web_page_preview=True)

    await Panel.delete.set()


@dp.message_handler(state=Panel.delete)
async def delete_get_id(message: types.Message, state: FSMContext):
    try:
        await db.delete_sponsor(int(message.text))
        await message.answer(text="✅ O'chirildi", reply_markup=start_admin)
        await state.finish()

    except ValueError as VE:
        logging.info(VE)
        await message.answer(text="Bu kanal yoki guruh topilmadi yoki id xato kiritilgan\n\nIltimos qaytadan yuboring",
                             reply_markup=back)