from math import ceil

from telethon.utils import get_display_name

import database
from domain import common
from domain.entities.users_meta import UsersMeta

_users_on_page = 5


@database.connection(False)
async def get_users(user_id: int, page: int = 1, c=None) -> UsersMeta:
    count, offset = _users_on_page, (page - 1) * _users_on_page
    total = database.privileges.get_users_count(user_id, c)
    data = UsersMeta(page=page, pages_count=ceil(total / count))

    if 0 < data.page <= data.pages_count:
        for id in database.privileges.get_users_page(user_id, offset, count, c):
            display_name = get_display_name(await common.client.get_entity(id))
            data.users.append(UsersMeta.User(id, display_name))

    return data


def get_user_data(owner_id: int, user_id: int):
    database.privileges.get_user_data()
    return None
