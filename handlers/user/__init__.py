import logging
import traceback
from asyncio import CancelledError

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import MessageNotModified, InvalidQueryID

import main_config
from handlers.user.default_handler import all_other_messages
from handlers.user.menu import start_handler, location_handler, confirm_location_handler, about_handler
from handlers.user.settings import settings_handler, change_settings_handler, set_notify_time_handler
from handlers.user.states import LocationOrder, NotifyOrder


def setup(dp: Dispatcher):
    dp.register_errors_handler(error_handler, exception=Exception)
    # main screen
    dp.register_message_handler(start_handler, commands='start')
    dp.register_callback_query_handler(start_handler, lambda clb: clb.data == 'menu', state='*')
    dp.register_callback_query_handler(about_handler, lambda clb: clb.data == 'about', state='*')
    dp.register_message_handler(location_handler, content_types=[types.ContentType.LOCATION, types.ContentType.TEXT],
                                state=LocationOrder.location_request)
    dp.register_message_handler(set_notify_time_handler, state=NotifyOrder.notify_time)
    dp.register_callback_query_handler(settings_handler, lambda clb: clb.data == 'settings')
    dp.register_callback_query_handler(confirm_location_handler,
                                       lambda clb: clb.data == 'geoconfirm',
                                       state=LocationOrder.location_request)
    dp.register_message_handler(all_other_messages, content_types=types.ContentType.ANY, state='*')

    # settings screen
    dp.register_callback_query_handler(change_settings_handler, lambda clb: clb.data.startswith('setchange_'))


async def left_handler(msg: types.Message):
    if msg.chat.id == 1:
        await msg.delete()


async def error_handler(upd: types.Update, ex: Exception):
    if isinstance(ex, MessageNotModified):
        return True
    elif isinstance(ex, CancelledError):
        return True
    elif isinstance(ex, InvalidQueryID):
        return True
    update = upd.message or upd.inline_query or upd.callback_query
    try:
        await upd.bot.send_message(main_config.ERROR_CHANNEL,
                               f'<pre><code class="language-python">{traceback.format_exc()}</code></pre>\n\nFrom: ({update.from_user.username or update.from_user.full_name}) {update.from_user.id}')
    except Exception as e:
        logging.info('Error: {}'.format(e))
        logging.error('Error: {}'.format(traceback.format_exc()))
    return True
