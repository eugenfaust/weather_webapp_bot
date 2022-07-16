import logging

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

import main_config
import filters
import handlers
from middlewares.acl import ACLMiddleware
from middlewares.throttle import ThrottlingMiddleware

logging.basicConfig(level=logging.INFO)
bot = Bot(token=main_config.API_TOKEN, parse_mode=types.ParseMode.HTML)
#storage = RedisStorage(main_config.REDIS_HOST, main_config.REDIS_PORT, main_config.REDIS_DB, main_config.REDIS_PASS)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
#dp.middleware.setup(ThrottlingMiddleware(1))
dp.middleware.setup(ACLMiddleware())

filters.setup(dp)

handlers.admin.setup(dp)
handlers.user.setup(dp)
