import logging
import random

from aiogram import types
from datetime import datetime

from aiogram.dispatcher.handler import SkipHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import main_config
from models.users import User


class ACLMiddleware(BaseMiddleware):

    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await User.query.where(User.uid == message.from_user.id).gino.first()
        if not user:
            ref_id = 0
            try:
                if message.text.startswith('/start'):
                    ref_id = int(message.text.split(' ')[1])
                    await message.bot.send_message(ref_id, '👤 У вас новый реферал: {}'
                                                   .format(message.from_user.full_name))
            except:
                pass
            user = await User.create(uid=message.from_user.id, status=False, created=datetime.now(),
                                     ref_id=ref_id, full_name=message.from_user.full_name)
        data['user'] = user

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        user = await User.query.where(User.uid == query.from_user.id).gino.first()
        if not user:
                user = await User.create(uid=query.from_user.id, status=False, created=datetime.now())
        data['user'] = user

    async def on_pre_process_inline_query(self, inline_query: types.InlineQuery, data: dict):
        user = await User.query.where(User.uid == inline_query.from_user.id).gino.first()
        if not user:
            user = await User.create(uid=inline_query.from_user.id, status=False, created=datetime.now())
        data['user'] = user

    async def on_post_process_message(self, message: types.Message, result, data: dict):
        await self.update_user(message.from_user, data['user'])

    async def on_post_process_callback_query(self, query: types.CallbackQuery, result, data: dict):
        await self.update_user(query.from_user, data['user'])

    async def on_post_process_inline_query(self, inline_query: types.InlineQuery, result, data: dict):
        await self.update_user(inline_query.from_user, data['user'])

    async def update_user(self, from_user, user: User):
        await user.update(last_action=datetime.now()).apply()
        if not user.username:
            if from_user.username:
                await user.update(username=from_user.username).apply()
        elif from_user.username:
            if user.username != from_user.username:
                await user.update(username=from_user.username).apply()