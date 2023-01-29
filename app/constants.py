week_day_map = {
    "Понедельник": 1,
    "Вторник": 2,
    "Среда": 3,
    "Четверг": 4,
    "Пятница": 5,
    "Суббота": 6,
    "Воскресенье": 7
}

weekday_map_vise_versa = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

# parser indexes
tags_index = 0
weekday_index = 1
time_index = 2
weeks_index = 3
subject_index = 4
subject_type_index = 5
professor_index = 6
classroom_index = 7
comment_index = 8

# date parsing patterns
schedule_date_pattern = '%d/%m/%Y'

# ---bot indexes---

# commands_base
callback_command_index = 1

# command_names
group_list_command = 'groups'


# ---enums---
class ScheduleMenuButtons:
    LEVEL = 'schedule'
    BACK = 'back'


class SettingsMenuButtons:
    LEVEL = 'settings'
    BACK = 'back'
    CHANGE_GROUP = 'change_group'
    BACK_PATTERN = f'{LEVEL}#{BACK}'
    CHANGE_GROUP_PATTERN = f'{LEVEL}#{CHANGE_GROUP}'


class MainMenuButtons:
    LEVEL = 'main_menu'
    HIDE = 'hide'
    SCHEDULE = 'schedule'
    SETTINGS = 'settings'
    HIDE_PATTERN = f'{LEVEL}#{HIDE}'
    SCHEDULE_PATTERN = f'{LEVEL}#{SCHEDULE}'
    SETTINGS_PATTERN = f'{LEVEL}#{SETTINGS}'
