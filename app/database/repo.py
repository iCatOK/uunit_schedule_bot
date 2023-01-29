import logging
from datetime import date

from .models import *
from app.config import peewee_sql, default_items_per_page
from app.utils import get_schedule_date

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')


class ConfigRepo:
    """
    Репозиторий конфигураций чатов
    """

    @staticmethod
    @peewee_sql
    def add_config(chat_id: int, group_name: str):
        """
        Добавить конфигурацию чата
        :param chat_id: Идентификатор чата
        :param group_name: Наименование группы
        """
        config = ChatConfig(chat_id=chat_id, group_name=group_name)
        res = config.save()
        logging.info("Configuration of chat #{0} is saved ({1})".format(chat_id, res))
        return True

    @staticmethod
    @peewee_sql
    def update_config(chat_id: int,
                      group_name: str = None):
        logging.info("Updating configuration of chat with id={}".format(chat_id))
        config, _ = ChatConfig.get_or_create(chat_id=chat_id)
        if group_name:
            config.group_name = group_name
        res = config.save()
        logging.info("Configuration of chat #{0} is updated ({1})".format(chat_id, res))

    @staticmethod
    @peewee_sql
    def get_config(chat_id: int):
        """
        Возвращает конфигурацию чата по идентификатору.
        :param chat_id: Идентификатор чата
        :return: Объект чата
        """
        return ChatConfig.get_or_none(ChatConfig.chat_id == chat_id)


class ScheduleRowRepo:
    """
    Репозиторий записей расписания
    """

    @staticmethod
    @peewee_sql
    def get_schedule_for_date(group: str, schedule_date: date):
        subject_iterator = ScheduleRow.select().where(
            ScheduleRow.date == schedule_date, ScheduleRow.group_name == group)
        subjects = list(subject_iterator)
        return subjects

    @staticmethod
    @peewee_sql
    def delete_all_schedule():
        ScheduleRow.delete().execute()

    @staticmethod
    def add_subject_rows(row: ScheduleRow, week_str: str, year: int):
        with db.atomic() as transaction:
            try:
                week_numbers = list(map(int, week_str.strip().split()))
                for week_number in week_numbers:
                    schedule_date = get_schedule_date(week_number, row.weekday, year)
                    new_subject_row = row.get_another_date_copy(schedule_date)
                    new_subject_row.save()
            except Exception as e:
                transaction.rollback()


class GroupRepo:
    """
    Репозиторий учебных групп
    """

    @staticmethod
    @peewee_sql
    def get_group_if_exists(group_name: str):
        return Group.select().get_or_none(group_name=group_name)

    @staticmethod
    @peewee_sql
    def add_group(group_id: int, group_name: str):
        group: Group = Group(group_name=group_name, group_id=group_id)
        group.save()

    @staticmethod
    @peewee_sql
    def delete_all_groups():
        Group.delete().execute()

    @staticmethod
    @peewee_sql
    def get_groups_of_page(page: int, items_per_page: int = default_items_per_page):
        return list(Group.select().order_by(Group.group_name).paginate(page, items_per_page))

    @staticmethod
    @peewee_sql
    def get_groups_page_count(items_per_page: int = default_items_per_page):
        count = Group.select().count()
        if count % items_per_page == 0:
            return count // items_per_page
        return count // items_per_page + 1
