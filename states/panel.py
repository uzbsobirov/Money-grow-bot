from aiogram.dispatcher.filters.state import State, StatesGroup


class Panel(StatesGroup):
    menu = State()

    # sponsor
    sponsor = State()
    get_data = State()
    delete = State()

    #add_card
    add_card = State()
    get_number = State()
    get_name = State()
    get_callback_data = State()
    get_owner_name = State()