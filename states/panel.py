from aiogram.dispatcher.filters.state import State, StatesGroup


class Panel(StatesGroup):
    menu = State()

    # sponsor
    sponsor = State()
    get_data = State()
    delete = State()

    # statistic
    statistic = State()

    # Answer to user
    answer_to_user = State()

    datas = State()