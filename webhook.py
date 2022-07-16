import logging
import time

from aiogram import Bot, Dispatcher, types
from aiohttp import web

import main_config
from bot import dp
from models import base, User


async def on_startup(web_app: web.Application):
    await base.on_startup(dp)
    await dp.bot.delete_webhook()
    await dp.skip_updates()
    await dp.bot.set_webhook(main_config.WEBHOOK_URL)


async def on_shutdown(web_app: web.Application):
    await base.on_shutdown(dp)

ban_list = {}


async def execute(req: web.Request) -> web.Response:
    updates = [types.Update(**(await req.json()))]
    for u in updates:
        cur_time = time.time()
        upd = u.message
        if upd:
            if upd.chat.type == types.ChatType.PRIVATE:
                user = upd.from_user
                if user is not None:
                    db_user = await User.query.where(User.uid == user.id).gino.first()
                    if db_user is None or not db_user.status:
                        if user.id in ban_list:
                            if cur_time - 2 < ban_list[user.id]:
                                logging.error('Banlist: banned user: {}'.format(user.id))
                                updates.remove(u)
                            else:
                                logging.error('Banlist: clear user: {}'.format(user.id))
                                ban_list.pop(user.id, None)
                        else:
                            logging.error('Banlist: new user: {}'.format(user.id))
                            ban_list[user.id] = cur_time
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    try:
        await dp.process_updates(updates)
    except Exception as e:
        logging.error(e)
    finally:
        return web.Response()


if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    app.add_routes([web.post('/', execute)])
    web.run_app(app, port=main_config.WEBAPP_PORT, host=main_config.WEBAPP_HOST)
