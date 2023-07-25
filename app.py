import asyncio

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.deposit_invest.purchase import scheduler


async def on_startup(dispatcher):
    await db.create()
    await db.create_table_users()
    await db.create_table_sponsor()
    await db.create_table_user_data()

    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    # asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
