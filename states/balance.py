from aiogram.dispatcher.filters.state import StatesGroup, State


class Balance(StatesGroup):
    balance = State()
