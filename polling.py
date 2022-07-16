from aiogram.utils import executor

from bot import dp
from models.base import on_startup, on_shutdown


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
