import logging
import os
from datetime import datetime

from telebot.types import InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator

from config import bot
from constants import MainMenuButtons, SettingsMenuButtons, ScheduleMenuButtons, schedule_date_pattern
from database.models import ChatConfig
from database.repo import GroupRepo, ConfigRepo
from menu import create_main_menu_markup, create_settings_markup, create_schedule_menu_markup
from schedule_parsing import generate_page_content, get_schedule_for_group, parse_all_groups_schedule


def send_groups_page(message, page: int = 1, edit: bool = False):
    group_page_count = GroupRepo.get_groups_page_count()
    page_text, buttons = generate_page_content(page)

    paginator = InlineKeyboardPaginator(
        group_page_count,
        current_page=page,
        data_pattern='groups#{page}'
    )

    for button in buttons:
        paginator.add_before(button)

    if edit:
        bot.edit_message_text(
            message.text,
            reply_markup=paginator.markup,
            chat_id=message.chat.id,
            message_id=message.message_id)
    else:
        bot.delete_message(
            message.chat.id,
            message.message_id
        )
        bot.send_message(
            message.chat.id,
            page_text,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )


@bot.message_handler(commands=['parse'])
def parse_schedule_data(message):
    chat_id = message.chat.id
    logging.info('{} {}'.format(chat_id, type(chat_id)))
    if message.chat.id == int(os.environ.get('ADMIN_CHAT_ID')):
        year = int(os.environ.get('UUNIT_YEAR'))
        semester = int(os.environ.get('UUNIT_SEMESTER'))
        parse_all_groups_schedule(year, semester)
        bot.send_message(
            message.chat.id,
            'Парсинг завершен',
        )


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == ScheduleMenuButtons.LEVEL)
def schedule_callback(call):
    command: str = call.data.split('#')[1]

    if command == ScheduleMenuButtons.BACK:
        bot.edit_message_text(
            'Основное меню:',
            reply_markup=create_main_menu_markup(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)
        return

    parsed_date = datetime.strptime(command, schedule_date_pattern).date()
    config: ChatConfig = ConfigRepo.get_config(call.message.chat.id)
    if not config:
        bot.edit_message_text(
            'Не удалось найти вашу группу. Основное меню:',
            reply_markup=create_main_menu_markup(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)
    message = get_schedule_for_group(config.group_name, parsed_date)
    bot.edit_message_text(
        message,
        reply_markup=create_schedule_menu_markup(),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == SettingsMenuButtons.LEVEL)
def settings_callback(call):
    command = call.data.split('#')[1]
    if command == SettingsMenuButtons.CHANGE_GROUP:
        send_groups_page(call.message, True)
    elif command == SettingsMenuButtons.BACK:
        bot.edit_message_text(
            'Основное меню:',
            reply_markup=create_main_menu_markup(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == MainMenuButtons.LEVEL)
def main_menu_callback(call):
    command = call.data.split('#')[1]
    config = ConfigRepo.get_config(call.message.chat.id)
    group = '' if not config else config.group_name
    if command == MainMenuButtons.HIDE:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif command == MainMenuButtons.SETTINGS:
        bot.edit_message_text(
            'Текущая группа: {}'.format(group),
            reply_markup=create_settings_markup(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)
    elif command == MainMenuButtons.SCHEDULE:
        bot.edit_message_text(
            'Выберите день:'.format(group),
            reply_markup=create_schedule_menu_markup(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'save_group')
def save_group_for_chat_callback(call):
    group_name = call.data.split('#')[1]
    ConfigRepo.update_config(call.message.chat.id, group_name)

    bot.send_message(
        call.message.chat.id,
        'Группа сохранена ({}). Теперь вы можете смотреть расписание'.format(group_name),
        reply_markup=create_main_menu_markup()
    )
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == 'groups')
def group_choosing_callback(call):
    page = int(call.data.split('#')[1])
    send_groups_page(call.message, page, True)


# Обработчик входящих сообщений
@bot.message_handler(content_types=['text'])
def start(message):
    chat_config = ConfigRepo.get_config(message.chat.id)
    logging.info('Chat id = {}'.format(message.chat.id))
    if chat_config:
        bot.send_message(
            message.chat.id,
            'Основное меню:',
            reply_markup=create_main_menu_markup()
        )
    else:
        send_groups_page(message)


