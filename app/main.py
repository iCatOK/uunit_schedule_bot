import logging
import os
import sys

import telebot

from config import init_db
from database.models import ScheduleRow, ChatConfig, Group
from bot import bot

current_dir = os.path.dirname(os.path.realpath(__file__))
main_folder_path = os.path.dirname(current_dir)
parent_dir = os.path.dirname(main_folder_path)
sys.path.append(os.path.dirname(parent_dir))
sys.path.append(current_dir)
sys.path.append(parent_dir)
sys.path.append(main_folder_path)


if __name__ == '__main__':
    init_db([ScheduleRow, ChatConfig, Group])
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Запуск бота"),
    ])

    # Set logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
    # Start the bot
    bot.polling(non_stop=True, interval=0)
