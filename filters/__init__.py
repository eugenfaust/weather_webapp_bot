from aiogram import Dispatcher

from filters.user import UserFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(UserFilter)