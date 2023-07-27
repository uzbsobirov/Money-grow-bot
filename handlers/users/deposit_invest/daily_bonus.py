from loader import db


async def job(user_id, tarif, balance, call, parent_id, user_data, bot):
    # if user_data[0][4] <= 0:
    print(123)
    await db.update_user_end_invest(user_id)
    new_balance = balance + tarif
    await db.update_user_balancee(balance=new_balance, user_id=user_id)
    await call.message.answer(text=f"Sizning hisobingizga {tarif} so'm qo'shildi")

    if parent_id:
        print(1234)
        await db.update_user_balanc(user_id=int(parent_id))
        await db.update_user_count(user_id=int(parent_id))
        await bot.send_message(
            chat_id=parent_id, text="Sizning hisobingizga 1500 so'm qo'shildi"
        )
                                                