import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.default.panel.menu import menues
from states.panel import Panel


@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = await db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@BekoDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)


@dp.message_handler(text="⌨️ Admin panel", state='*', user_id=ADMINS[0])
async def admin_panel(message: types.Message, state: FSMContext):
    text = "<b>Admin panelga xush kelibsiz👣</b>"
    await message.answer(text=text, reply_markup=menues)
    await Panel.menu.set()