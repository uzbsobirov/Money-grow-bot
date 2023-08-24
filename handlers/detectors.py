from typing import Union

from keyboards.default.start import start_user, start_admin
from data.config import ADMINS


async def detect_is_admin(user_id: Union[str, int]):
    if int(user_id) == int(ADMINS[0]):
        return start_admin
    else:
        return start_user


def detect_type_name(data):
    if data == 'one':
        return 'Vib 1', 30000, 75000, 2500, 30

    elif data == 'two':
        return 'Vib 2', 60000, 150000, 5000, 30

    elif data == 'three':
        return 'Vib 3', 150000, 390000, 13000, 30

    elif data == 'four':
        return 'Vib 4', 250000, 630000, 21000, 30

    elif data == 'five':
        return 'Vib 5', 360000, 930000, 31000, 30

    elif data == 'six':
        return 'Vib 6', 650000, 1650000, 55000, 30

    elif data is None:
        return ['Siz xarid qilmadingiz❌']


def detect_user_balance(data, balance):
    if data == 'one':
        if balance >= 30000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'two':
        if balance >= 60000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'three':
        if balance >= 150000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'four':
        if balance >= 250000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'five':
        if balance >= 360000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'six':
        if balance >= 650000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"
