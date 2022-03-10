from datetime import datetime
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

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

    # @property
    # def calc_time2(self):
    #     today = datetime.date.today()
    #     d_start = datetime.datetime.combine(today, self.started_at)
    #     d_end = datetime.datetime.combine(today, self.ended_at)
    #     diff = d_end - d_start
    #     return diff

    # def calc_time(self, start, end):
    #     today = datetime.date.today()
    #     d_start = datetime.datetime.combine(today, start)
    #     d_end = datetime.datetime.combine(today, end)
    #     diff = d_end - d_start
    #     return diff

    #different = substract_time(self)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="actions")

    def __str__(self):
        return self.name