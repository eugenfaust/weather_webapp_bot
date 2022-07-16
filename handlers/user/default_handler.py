import asyncio
import json
import logging
import random
import re
import time
from datetime import datetime, timedelta

import aiohttp
import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BotBlocked
from aiohttp import ClientHttpProxyError

import main_config
from models.users import User


async def all_other_messages(message: types.Message):
    await message.answer('Hello')


class SampleOrder(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()