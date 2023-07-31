from aiogram.dispatcher.filters.state import StatesGroup, State


class Balance(StatesGroup):
    menu = State()

    deposit = State()
    checkout = State()

    withdraw = State()
    money = State()

    id = State()

    cancel_payment = State()


class Payment(StatesGroup):
    payment_time = State()

