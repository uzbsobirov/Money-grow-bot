from aiogram.dispatcher.filters.state import StatesGroup, State


class Balance(StatesGroup):
    menu = State()

    deposit = State()
    checkout = State()