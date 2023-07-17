from typing import Union

from keyboards.default.start import start_user, start_admin
from data.config import ADMINS


async def detect_is_admin(user_id: Union[str, int]):
    if user_id == int(ADMINS[0]):
        return start_admin
    else:
        return start_user


def detect_type_name(data):
    if data == 'one':
        return 'Vib 1', 100000, 175000, 5000, 35

    elif data == 'two':
        return 'Vib 2', 140000, 245000, 7000, 35

    elif data == 'three':
        return 'Vib 3', 250000, 455000, 13000, 35

    elif data == 'four':
        return 'Vib 4', 500000, 910000, 26000, 35

    elif data == 'five':
        return 'Vib 5', 840000, 1575000, 45000, 35

    elif data == 'six':
        return 'Vib 5', 1300000, 2450000, 70000, 35


def detect_user_balance(data, balance):
    if data == 'one':
        if balance >= 100000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'two':
        if balance >= 140000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'three':
        if balance >= 250000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'four':
        if balance >= 500000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'five':
        if balance >= 840000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"

    elif data == 'six':
        if balance >= 1300000:
            return True

        else:
            return "⚠️ Mablag' yetarli emas"
