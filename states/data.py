from aiogram.dispatcher.filters.state import StatesGroup, State


class Data(StatesGroup):
    information = State()

    investors = State()