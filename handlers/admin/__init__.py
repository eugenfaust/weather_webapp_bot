import time
import datetime

from aiogram import Dispatcher, types
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

import main_config


def setup(dp: Dispatcher):
    dp.register_message_handler(setup_commands, lambda msg: msg.from_user.id == main_config.ERROR_CHANNEL,
                                commands='setup', state='*')


async def get_sticker_id(msg: types.Message):
    await msg.answer('ID: {}'.format(msg.sticker.file_unique_id))


async def setup_commands(msg: types.Message):
    commands = [BotCommand('menu', 'Показать меню')]
    await msg.bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())
    # VBIV
    commands = [BotCommand('menu', 'Показать меню'),
                BotCommand('admin', 'Показать admin'),]
    await msg.bot.set_my_commands(commands, BotCommandScopeChat(main_config.ERROR_CHANNEL))
    await msg.answer('Команды установлены')