from datetime import datetime, timedelta, date
import datetime
from msilib.schema import Error
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db.models.functions import Upper

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    #action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', Upper('title')]

class Action(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    started_at=models.TimeField()
    ended_at=models.TimeField()

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="actions")

    def __str__(self):
        return self.name

    @property
    def calc_time_substract(self):
        date = datetime.date(1, 1, 1)
        d_start = datetime.datetime.combine(date, self.started_at)
        d_end = datetime.datetime.combine(date, self.ended_at)
        print(type(d_start), type(d_end))
        time_elapsed = d_end - d_start
        return time_elapsed

    @staticmethod
    def format_timedelta(delta: timedelta) -> str:
        seconds = int(delta.total_seconds())

        secs_in_a_hour = 3600
        secs_in_a_min = 60

        hours, seconds = divmod(seconds, secs_in_a_hour)
        minutes, seconds = divmod(seconds, secs_in_a_min)
        
        print(hours)
        print(minutes)
        
        
        if minutes == 0:
            suffix = "s" if hours > 1 else ""
            return f"{hours} hour{suffix}"
        if minutes > 0 and hours < 1:
            suffix = "s" if minutes > 1 else ""
            return f"{minutes} minute{suffix}"
        if hours > 0:
            suffix_h = "s" if hours > 1 else ""
            suffix_m = "s" if minutes > 1 else ""
            time_fmt = f"{minutes:02d}" if minutes > 9 else f"{minutes:01d}"
            return f"{hours} hour{suffix_h} {time_fmt} minute{suffix_m}"

        return time_fmt

    class Meta:
            ordering = [Upper('name')]