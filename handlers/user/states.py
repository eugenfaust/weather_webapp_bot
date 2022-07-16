from aiogram.dispatcher.filters.state import StatesGroup, State


class LocationOrder(StatesGroup):
    location_request = State()


class NotifyOrder(StatesGroup):
    notify_time = State()
