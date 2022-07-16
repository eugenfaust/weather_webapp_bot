import random
import subprocess
import asyncio
import os
from datetime import datetime, timedelta

import pytz
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ChatInviteLink

import main_config

async def cmd_work(msg: types.Message):
    pass