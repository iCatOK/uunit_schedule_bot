from datetime import datetime, date
from itertools import cycle

import isoweek

from app.constants import week_day_map


def get_actual_date_parts(week_number: int, academic_year: int):
    last_week_of_year = isoweek.Week.last_week_of_year(academic_year).week
    actual_week_number = week_number + 35 - 1
    if actual_week_number > last_week_of_year:
        academic_year += 1
        actual_week_number -= last_week_of_year
    return actual_week_number, academic_year


def get_schedule_date(week_number: int, week_day: str, academic_year: int):
    actual_week_number, actual_year = get_actual_date_parts(week_number, academic_year)
    date_str = f"{actual_year}-W{actual_week_number}"
    week_day_number = week_day_map[week_day]
    return datetime.strptime(date_str + f'-{week_day_number}', "%Y-W%W-%w").date()


def get_date_by_weekday(data: dict):
    weekday = data['weekday']
    weekday_number = week_day_map[weekday] - 1
    week = isoweek.Week.thisweek()
    today_day_number = date.today().weekday()
    if weekday_number <= today_day_number:
        week += 1
    return week.day(weekday_number)


def get_button_descriptions():
    today_weekday = date.today().weekday()
    weekdays = cycle(['Понедельник', 'Вторник', 'Среда', "Четверг", "Пятница", "Суббота"])
    for i in range(today_weekday):
        next(weekdays)
    return [next(weekdays) for _ in range(6)]


if __name__ == '__main__':
    print(get_button_descriptions())
