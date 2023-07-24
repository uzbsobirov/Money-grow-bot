import asyncio
import logging

import asyncpg

from data.config import ADMINS
from keyboards.default.start import start_admin
from loader import dp, db, bot
from states.panel import Panel

from aiogram.dispatcher import FSMContext
from aiogram import types


@dp.message_handler(text="🗞 Reklama yuborish", user_id=ADMINS[0], state=Panel.menu)
async def repost(message: types.Message, state: FSMContext):
    await message.answer("<b>Reklamani yuboring...</b>")
    await Panel.datas.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, user_id=ADMINS, state=Panel.datas)
async def send_post_all_groups(message: types.Message, state: FSMContext):
    users = await db.select_all_users()

    admin_text = "<b>🔖Reklama <code>{}</code> ta foydalanuvchiga yuborish boshlandi</b>".format(len(users))
    await message.answer(text=admin_text)

    sended = 0
    unsended = 0

    try:
        for user in users:
            user_id = user[3]
            try:
                await message.send_copy(chat_id=user_id)
                sended += 1
                await asyncio.sleep(0.05)
            except Exception as error:
                logging.info(error)
                unsended += 1
                continue

    except asyncpg.exceptions as error:
        logging.info(error)
        await message.answer("Uzur xatolik yuz berdi, keyinroq urinib ko'ring!")

    except Exception as error:
        logging.info(error)
        pass

    finally:
        response = "✅ Reklama {} / {} ta foydalanuvchiga yuborildi\n\n" \
                   "❌ Reklama {} / {} ta foydalanuvchiga yuborilmadi".format(sended, len(users), unsended, len(users))
        await message.answer(text=response, reply_markup=start_admin)
        await state.finish()