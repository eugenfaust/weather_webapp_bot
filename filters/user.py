from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from models import User


@dataclass
class UserFilter(BoundFilter):
    key = 'is_user'
    is_user: bool

    async def check(self, *args) -> bool:
        data = ctx_data.get()
        if 'user' in data:
            user: User = data['user']
            return user.status
        return False
