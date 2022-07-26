import datetime as dt
import math

from aiogram import types

import utils.constants as const
from config.bot_config import bot
from config.telegram_config import CHAT_ID
from functions.plan_check import plan_tu_check
from functions.request_weather import request_weather
from functions.scrap_history_day import scrap_history_day
from functions.second_level_apk_check import second_level_apk_check
from functions.text_generators import (evening_hello_generator,
                                       hello_generator, month_plan_generator,
                                       wish_generator)
from texts.apk import APK_2_REMAINDER


async def send_morning_hello():
    month = str(dt.datetime.today().month)
    day = dt.datetime.today().day
    if day == 31:
        day_trinity = '10'
    else:
        day_trinity = str(math.ceil(day/3))
    avo_temp = const.RECOMMEND_TEMP[month][day_trinity]
    text_avo_temp = (
        f'Рекомендуемая температура газа после АВО:\n{avo_temp} град. Цельсия'
    )
    text_morning_hello = hello_generator()
    text_weather = request_weather()
    message = '{}\n{}\n{}'.format(
        text_morning_hello,
        text_weather,
        text_avo_temp,
    )
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def send_evening_hello():
    text_evening_hello = evening_hello_generator()
    text_weather = request_weather()
    message = '{}\n{}'.format(
        text_evening_hello,
        text_weather
    )
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def send_morning_wish():
    now_day = dt.datetime.today().day
    if now_day == 1:
        text_month_plan = month_plan_generator()
    else:
        text_month_plan = ''
    message = '{}\n\n{}'.format(wish_generator(), text_month_plan)
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def send_history_day():
    text_history_day = scrap_history_day()
    prefix = 'Доставайте чай, наливайте печенюшки'
    full_text = '{}\n\n{}'.format(prefix, text_history_day)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=full_text,
        parse_mode=types.ParseMode.HTML
    )


async def send_apk_2_remainder():
    # в ответе функции second_apk_check приходит словарь
    check = second_level_apk_check().get('check')
    if check:
        today = second_level_apk_check().get('date')
        weekday = second_level_apk_check().get('weekday')
        text_today = f'Сегодня {today} число месяца, {weekday}.'
        message = '{}\n{}'.format(text_today, APK_2_REMAINDER)
        await bot.send_message(chat_id=CHAT_ID, text=message)


async def send_tu_theme():
    check = plan_tu_check().get('check')
    if check:
        list_tu = plan_tu_check().get('data')
        text = ''
        for theme in list_tu:
            text = '{}\n{}\n'.format(text, theme)
        message = (
            f'Сегодня по плану должна быть техучёба.\nТемы занятий:\n{text}'
        )
        await bot.send_message(chat_id=CHAT_ID, text=message)
