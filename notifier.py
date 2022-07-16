import asyncio
import datetime

import pytz
from aiogram import Bot, types
from sqlalchemy import func

import main_config
from models import Reminder, User
from models.base import on_startup, on_shutdown
from services.weather import WeatherService


async def check_notifies():
    await on_startup()
    bot = Bot(token=main_config.API_TOKEN, parse_mode=types.ParseMode.HTML)
    cur_time = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))
    reminders = await Reminder.query.where(func.date_part('hour', Reminder.notify_time) == cur_time.hour)\
        .where(func.date_part('minute', Reminder.notify_time) == cur_time.minute).gino.all()
    #
    print(cur_time)
    if reminders:
        for reminder in reminders:
            user = await User.query.where(User.uid == reminder.user_id).gino.first()
            weather = WeatherService(user.location, user.city_name)
            current_weather = weather.get_current_weather()
            text = "✋ Привет!\n" \
                   f"📅 Сейчас в <b>{user.city_name.strip()}</b> {current_weather['description']}\n" \
                   f"🌡️ Температура: {current_weather['temp']}°C\n" \
                   f"🙂 Ощущается как: {current_weather['feels']}°C"
            try:
                await bot.send_message(reminder.user_id, text)
            except:
                pass
    await on_shutdown()

loop = asyncio.get_event_loop()
loop.run_until_complete(check_notifies())
