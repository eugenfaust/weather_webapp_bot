import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.user.states import LocationOrder, NotifyOrder
from handlers.user.markups import get_settings, get_cancel
from models import User, Reminder


async def settings_handler(clb: types.CallbackQuery, user: User):
    await clb.answer()
    await clb.message.delete()
    await clb.message.answer('Что будете настраивать?', reply_markup=get_settings())


async def change_settings_handler(clb: types.CallbackQuery, user: User):
    await clb.answer()
    setting = clb.data.split('_')[1]
    if setting == 'geo':
        await clb.message.answer('В каком городе ты хотел бы отслеживать погоду?\n'
                                 'Напиши название города или поделись своей локацией с нами.',
                                 reply_markup=get_cancel())
        await LocationOrder.location_request.set()
    elif setting == 'notify':
        await clb.message.answer('В какое время ты хотел бы получать уведомление о погоде?\n'
                                 'Напиши время в формате HH:MM.',
                                 reply_markup=get_cancel())
        await NotifyOrder.notify_time.set()
    else:
        await clb.message.answer('Возникла ошибка, возможно эта настройка еще не реализована.')


async def set_notify_time_handler(msg: types.Message, user: User, state: FSMContext):
    if len(msg.text) == 5:
        if ':' in msg.text:
            notify_time = msg.text.split(':')
            hh = notify_time[0]
            mm = notify_time[1]
            try:
                if hh.startswith('0'):
                    hh = hh[-1]
                if mm.startswith('0'):
                    mm = mm[-1]
                notify_date = datetime.datetime.now().replace(hour=int(hh), minute=int(mm))
                await Reminder.create(user_id=user.uid, notify_time=notify_date)
                await state.finish()
                await msg.answer('Уведомления установлены на {} часов'.format(msg.text), reply_markup=get_cancel())
            except:
                await msg.answer('Неверный ввод. Попробуй еще раз. Формат времени - НН:ММ', reply_markup=get_cancel())
    else:
        await msg.answer('Неверный ввод. Попробуй еще раз. Формат времени - НН:ММ', reply_markup=get_cancel())