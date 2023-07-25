from loader import db


async def job(user_id, tarif, balance, call):
    await db.update_user_end_invest(user_id)
    new_balance = balance + tarif
    await db.update_user_balancee(balance=new_balance, user_id=user_id)
    await call.message.answer(text=f"Sizning hisobingizga {tarif} so'm qo'shildi")
