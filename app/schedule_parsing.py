from datetime import datetime, date as dt, timedelta

import requests
from bs4 import BeautifulSoup
from lxml import etree
from telebot.types import InlineKeyboardButton

from constants import tags_index, weekday_index, subject_type_index, professor_index, comment_index, \
    classroom_index, weeks_index, time_index, subject_index, schedule_date_pattern
from database.models import ScheduleRow, Group
from database.repo import ScheduleRowRepo, GroupRepo
from utils import get_date_by_weekday
from config import init_db, default_items_per_page

command_map = {
    "Сегодня": lambda _: dt.today(),
    "Завтра": lambda _: dt.today() + timedelta(days=1),
    "Понедельник": get_date_by_weekday,
    "Вторник": get_date_by_weekday,
    "Среда": get_date_by_weekday,
    "Четверг": get_date_by_weekday,
    "Пятница": get_date_by_weekday,
    "Суббота": get_date_by_weekday
}


def save_schedule_for_group(schedule_data, academic_year, group_name, group_id):
    week_day = 'Понедельник'
    subject_order = 0
    for schedule_row in schedule_data:
        subject_order += 1
        if 'dayheader' in schedule_row[tags_index]:
            week_day = schedule_row[weekday_index]
            subject_order = 1
        if 'noinfo' in schedule_row[tags_index]:
            continue
        if 'dayheader' in schedule_row[tags_index] or 'extra' in schedule_row[tags_index]:
            row = ScheduleRow(
                date=dt.today(),
                weekday=week_day,
                time=schedule_row[time_index],
                subject_order=subject_order,
                group_name=group_name,
                group_id=group_id,
                subject=schedule_row[subject_index],
                subject_type=schedule_row[subject_type_index],
                professor=schedule_row[professor_index],
                classroom=schedule_row[classroom_index],
                comment=schedule_row[comment_index]
            )
            ScheduleRowRepo.add_subject_rows(row, schedule_row[weeks_index], academic_year)


def parse_all_groups_schedule(academic_year: int, semester: int):
    base_url = get_semester_url(academic_year, semester)
    groups = parse_groups(base_url)
    GroupRepo.delete_all_groups()
    ScheduleRowRepo.delete_all_schedule()
    for group_id, group_name in groups.items():
        if group_name == '0':
            continue
        GroupRepo.add_group(group_id, group_name)
        group_url = base_url + f"&student_group_id={group_id}"
        schedule_data = parse_schedule(group_url)
        save_schedule_for_group(schedule_data, academic_year, group_name, group_id)
        break


def get_semester_url(academic_year: int, semester: int):
    date = datetime(academic_year, 1, 1).strftime('%y')
    return f'https://isu.ugatu.su/api/new_schedule_api/' \
           f'?schedule_semestr_id={date}{semester}&WhatShow=1'


def parse_groups(url: str) -> dict:
    headers = {'Accept-Encoding': 'gzip, deflate, br'}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    dom = etree.HTML(str(soup))
    groups = dom.xpath('//select[@name="student_group_id"]/option')
    return {x.attrib['value']: x.text for x in groups}


def parse_schedule(url: str):
    headers = {'Accept-Encoding': 'gzip, deflate, br'}
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, "lxml")
    trs = soup.find('table').find_all('tr')
    schedule_matrix = []

    for tr in trs:
        tds = tr.find_all('td')
        row = list(map(lambda x: x.text, tds))
        if tr.has_attr('class'):
            row.insert(0, tr['class'])
        schedule_matrix.append(row)
    return schedule_matrix[1:]


def get_schedule_for_group(group_name: str, date: dt):
    subs = ScheduleRowRepo.get_schedule_for_date(group_name, date)
    if len(subs) > 0:
        return 'Расписание на {}\n\n{}'.format(
            date.strftime(schedule_date_pattern),
            '\n\n'.join([str(s) for s in subs])
        )
    else:
        return 'Нет информации по дате {}'.format(date.strftime(schedule_date_pattern))


def generate_page_content(current_page: int, items_per_page: int = default_items_per_page):
    groups = GroupRepo.get_groups_of_page(current_page, items_per_page)
    header = 'Выберите группу\n\n'
    group_buttons = [
        InlineKeyboardButton(f'{g.group_name}', callback_data='save_group#{}'.format(g.group_name))
        for g in groups
    ]
    return '{}'.format(header), group_buttons


if __name__ == '__main__':
    init_db([ScheduleRow, Group])
    parse_all_groups_schedule(2022, 2)
