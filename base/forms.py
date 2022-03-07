from .models import Action, Task
from django import forms


class Form1(forms.ModelForm):
   class Meta:
        model = Action
        fields = '__all__'


class Form2(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title',
                  'description',
                  'complete',
                                ]
