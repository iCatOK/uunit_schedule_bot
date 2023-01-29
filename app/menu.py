import locale
import logging
from datetime import date, timedelta

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants import *

locale.setlocale(locale.LC_ALL, 'ru_RU')


def create_schedule_menu_markup():
    locale.setlocale(locale.LC_ALL, 'ru_RU')
    logging.info("locale = {}".format(locale.getlocale()))
    day = date.today()
    pattern = schedule_date_pattern
    day_str = day.strftime(pattern)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text=f'Сегодня', callback_data='{}#{}'.format(ScheduleMenuButtons.LEVEL, day_str))
    )
    days_count = 0
    while days_count < 5:
        day += timedelta(days=1)
        weekday = day.weekday()

        if weekday == 6:
            continue

        weekday_str = weekday_map_vise_versa[weekday]

        day_str = day.strftime(pattern)
        markup.add(
            InlineKeyboardButton(text=weekday_str, callback_data='{}#{}'.format(ScheduleMenuButtons.LEVEL, day_str))
        )
        days_count += 1
    markup.add(
        InlineKeyboardButton(text=f'Назад', callback_data='{}#{}'.format(
            ScheduleMenuButtons.LEVEL,
            ScheduleMenuButtons.BACK))
    )
    return markup


def create_settings_markup():
    markup = InlineKeyboardMarkup()

    buttons = [
        InlineKeyboardButton(text=f'Изменить группу', callback_data=SettingsMenuButtons.CHANGE_GROUP_PATTERN),
        InlineKeyboardButton(text=f'Назад', callback_data=SettingsMenuButtons.BACK_PATTERN),
    ]

    for button in buttons:
        markup.add(button)

    return markup


def create_main_menu_markup():
    markup = InlineKeyboardMarkup()

    buttons = [
        InlineKeyboardButton(text=f'Расписание', callback_data=MainMenuButtons.SCHEDULE_PATTERN),
        InlineKeyboardButton(text=f'Настройки', callback_data=MainMenuButtons.SETTINGS_PATTERN),
        InlineKeyboardButton(text=f'Скрыть', callback_data=MainMenuButtons.HIDE_PATTERN)
    ]

    for button in buttons:
        markup.add(button)

    return markup
