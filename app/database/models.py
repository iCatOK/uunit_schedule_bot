import datetime

from peewee import *

from app.config import db


class Group(Model):
    """
    Учебная группа
    """
    group_id = IntegerField(unique=True)
    group_name = TextField(null=True)

    class Meta:
        database = db
        table_name = 'groups'


class ChatConfig(Model):
    """
    Конфигурация чата
    """
    chat_id = IntegerField(unique=True)
    group_name = TextField(null=True)

    class Meta:
        database = db
        table_name = 'configs'


class ScheduleRow(Model):
    """
    Предмет расписания
    """
    date = DateField(null=True)
    weekday = TextField(null=True)
    time = TextField(null=True)
    subject_order = IntegerField(null=True)
    group_name = TextField(null=True)
    group_id = IntegerField(null=True)
    subject = TextField(null=True)
    subject_type = TextField(null=True)
    professor = TextField(null=True)
    classroom = TextField(null=True)
    comment = TextField(null=True, default="")

    def __str__(self):
        return f"[{self.subject_order} пара] ({self.time})\n\n" \
               f"{self.subject}\n" \
               f"Аудитория: {self.classroom}\n" \
               f"Тип занятия: {self.subject_type}\n" \
               f"Преподаватель: {self.professor}"

    def get_another_date_copy(self, schedule_date: datetime.date):
        row = ScheduleRow(date=schedule_date,
                          weekday=self.weekday,
                          time=self.time,
                          subject_order=self.subject_order,
                          group_name=self.group_name,
                          group_id=self.group_id,
                          subject=self.subject,
                          subject_type=self.subject_type,
                          professor=self.professor,
                          classroom=self.classroom,
                          comment=self.comment)
        return row

    class Meta:
        database = db
        table_name = 'schedule_rows'
