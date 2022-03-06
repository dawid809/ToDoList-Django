from django.contrib import admin
from .models import Action, Task

# Register your models here.
admin.site.register(Task)
admin.site.register(Action)