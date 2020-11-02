import datetime
from django.db import models
from django.utils import timezone


class Schedule(models.Model):
    """スケジュール"""
    summary = models.CharField('Schedule', max_length=50)
    #description = models.TextField('詳細な説明', blank=True)
    start_time = models.TimeField('Alarm', default=timezone.now)
    end_time = models.TimeField('WakeUp', blank=True, null=True)
    date = models.DateField('日付')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.summary
