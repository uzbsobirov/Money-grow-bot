from aiogram.dispatcher.filters.state import State, StatesGroup


class Panel(StatesGroup):
    menu = State()

    # sponsor
    sponsor = State()
    get_data = State()
    delete = State()

    # statistic
    statistic = State()