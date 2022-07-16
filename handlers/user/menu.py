from typing import Union

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.user.states import LocationOrder
from handlers.user.markups import get_menu, get_geo_confirm, get_about
from main_config import WEATHER_GEOCODING_URL, WEATHER_GEODECODING_URL, DEVELOPER_USERNAME
from models import User
from services.geocode import get_location_by_name, get_location_by_coord


async def start_handler(msg: Union[types.Message, types.CallbackQuery], user: User, state):
    await state.finish()
    message = msg
    if isinstance(msg, types.CallbackQuery):
        await msg.answer()
        await msg.message.delete()
        message = msg.message
    if user.location:
        await message.answer('Привет, <b>{}</b>!\n'.format(user.full_name), reply_markup=get_menu(user))
    else:
        await message.answer('Добро пожаловать, <b>{}</b>!\n'
                         'В каком городе ты хотел бы отслеживать погоду?\n'
                         'Напиши название города или поделись своей локацией с нами.'.format(user.full_name))
        await LocationOrder.location_request.set()


async def location_handler(msg: types.Message, user: User, state: FSMContext):
    if msg.content_type == types.ContentType.LOCATION:
        result = get_location_by_coord(msg.location.latitude, msg.location.longitude)
        if not result:
            await msg.answer('Что-то пошло не так, попробуй ввести название города вручную')
            return

        await user.update(location=f"{result['lat']},{result['lon']}", city_name=result['city_name']).apply()
        await state.finish()
        await msg.answer('Город {} установлен!\n'
                         'Посмотрим погоду?'.format(user.city_name), reply_markup=get_menu(user))
    else:
        location = get_location_by_name(msg.text)
        if not location:
            await msg.answer('Такого города, к сожалению, не найдено. Попробуй указать точнее.')
        else:
            location_coord = f"{location['lat']},{location['lon']}"
            city_name = location['city_name']
            await state.update_data(location=location_coord, city_name=city_name)
            await msg.answer('Твой город - <u>{}</u>. Я все верно понял?\n'
                             'Если неверно - попробуй написать еще раз.'.format(city_name),
                             reply_markup=get_geo_confirm())


async def confirm_location_handler(clb: types.CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    coords = data['location']
    city_name = data['city_name']
    await state.finish()
    await clb.answer()
    await clb.message.delete()
    await user.update(location=coords, city_name=city_name).apply()
    await clb.message.answer('Город установлен!\n'
                     'Посмотрим погоду?', reply_markup=get_menu(user))


async def about_handler(clb: types.CallbackQuery):
    text = 'Разработчик бота - {}\n' \
           'Если есть желание поддержать копейкой, нажмите кнопку внизу :)'.format(DEVELOPER_USERNAME)
    kb = get_about()
    await clb.answer()
    await clb.message.delete()
    await clb.message.answer(text, reply_markup=kb)