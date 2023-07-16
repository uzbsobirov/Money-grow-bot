from typing import Union

from keyboards.default.start import start_user, start_admin
from data.config import ADMINS


async def detect_is_admin(user_id: Union[str, int]):
    if user_id == int(ADMINS[0]):
        return start_admin
    else:
        return start_user


def detect_type_name(data):
    if data == 'temir':
        return '⚫️ Temir', 100000, 175000, 5000, 35

    elif data == 'bronza':
        return '🟤 Bronza'

    elif data == 'kumush':
        return '🔘 Kumush'

    elif data == 'olmos':
        return '🟡 Oltin'

    elif data == 'oltin':
        return '💎 Olmos'
