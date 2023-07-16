from aiogram.dispatcher.filters.state import StatesGroup, State


class Invest(StatesGroup):
    types = State()