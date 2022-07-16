from aiogram import types

from main_config import WEATHER_NOW, WEATHER_WEEK, DONATE_URL, SOURCE_URL
from models import User


def get_menu(user: User) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)

    kb.add(types.InlineKeyboardButton('Сегодня', web_app=types.WebAppInfo(url=WEATHER_NOW.format(user.uid))))
    kb.add(types.InlineKeyboardButton('На ближайшие дни', web_app=types.WebAppInfo(url=WEATHER_WEEK.format(user.uid))))

    kb.add(types.InlineKeyboardButton('Настройки', callback_data='settings'))
    kb.add(types.InlineKeyboardButton('О боте', callback_data='about'))
    return kb


def get_geo_confirm() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton('Да!', callback_data='geoconfirm'))
    return kb


def get_settings() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Изменить город', callback_data='setchange_geo'))
    kb.add(types.InlineKeyboardButton('Уведомление', callback_data='setchange_notify'))
    kb.add(_get_back_button())
    return kb


def get_about() -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Поддержать', url=DONATE_URL))
    kb.add(types.InlineKeyboardButton('Исходный код', url=SOURCE_URL))
    kb.add(_get_back_button())
    return kb


def get_cancel()  -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup()
    kb.add(_get_back_button())
    return kb


def _get_back_button() -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton('Назад', callback_data='menu')