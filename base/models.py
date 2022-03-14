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



    # def clean(self):

    #     if self.cleaned_data['started_at'] >= self.cleaned_data['ended_at']:
    #         print('start greate than end')
    #         raise Error("start > end")

    # def clean(self):
    #     print('self', self.cleaned_data.get('started_at'))
            #raise ValidationError({"ended_at": "End date must be higher than start date!"})

    # @property
    # def calc_time(self):
    #     today = datetime.date.today()
    #     d_start = datetime.datetime.combine(today, self.started_at)
    #     d_end = datetime.datetime.combine(today, self.ended_at)
    #     diff = d_end - d_start
    #     return diff

    @property
    def calc_time2(self):
        date = datetime.date(1, 1, 1)
        d_start = datetime.datetime.combine(date, self.started_at)
        d_end = datetime.datetime.combine(date, self.ended_at)
        print(type(d_start), type(d_end))
        # if d_start > d_end:
        #     time_elapsed = d_start - d_end
        # else:
        time_elapsed = d_end - d_start
        return time_elapsed

    def cs_print(self):
        print('wywołano')

    def format_timedelta(delta: timedelta) -> str:

        seconds = int(delta.total_seconds())

        secs_in_a_day = 86400
        secs_in_a_hour = 3600
        secs_in_a_min = 60

        days, seconds = divmod(seconds, secs_in_a_day)
        hours, seconds = divmod(seconds, secs_in_a_hour)
        minutes, seconds = divmod(seconds, secs_in_a_min)

        time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        if days > 0:
            suffix = "s" if days > 1 else ""
            return f"{days} day{suffix} {time_fmt}"

        return time_fmt

    # def calc_time(self, start, end):
    #     today = datetime.date.today()
    #     d_start = datetime.datetime.combine(today, start)
    #     d_end = datetime.datetime.combine(today, end)
    #     diff = d_end - d_start
    #     return diff

    #different = substract_time(self)