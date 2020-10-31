import datetime
from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('Schedule', max_length=50)
    #description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('Alarm', default=None)
    end_time = models.TimeField('WakeUp', default=timezone.now)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary

class Options(models.Model):
    #todo_id = models.CharField(unique=True, max_length=5)
    default_alarm = models.BooleanField('Default_alarm')
    default_time = models.TimeField('Default_time')
    method_servo = models.BooleanField('Servo')
    method_sound = models.BooleanField('Sound')
