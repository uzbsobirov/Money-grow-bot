from loader import db, bot


async def job(user_id, tarif, call, scheduler):
    user_data = await db.select_user_data(user_id=user_id)
    end_invest = user_data[0][4]

    if end_invest > 0:
        print(end_invest)
        balance = user_data[0][2]
        parent_id = user_data[0][5]

        await db.update_user_end_invest(user_id)
        new_balance = balance + tarif
        await db.update_user_balancee(balance=new_balance, user_id=user_id)
        await call.message.answer(text=f"Sizning hisobingizga {tarif} so'm qo'shildi")

        if parent_id:
            await db.update_user_balanc(user_id=int(parent_id))
            await db.update_user_count(user_id=int(parent_id))
            await bot.send_message(
                chat_id=parent_id, text="Sizning hisobingizga 1500 so'm qo'shildi"
            )

    elif end_invest == 0 or end_invest < 0:
        scheduler.shutdown()


