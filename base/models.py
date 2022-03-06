from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

from django.db.models.functions import Upper

# Create your models here.

class Action(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    started_at=models.DateTimeField()
    ended_at=models.DateTimeField()


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    action = models.ForeignKey(Action, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', Upper('title')]