import os

from app.schedule_parsing import parse_all_groups_schedule

if __name__ == '__main__':
    year = int(os.environ.get('UUNIT_YEAR'))
    semester = int(os.environ.get('UUNIT_SEMESTER'))
    parse_all_groups_schedule(year, semester)

