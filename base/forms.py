from collections import UserDict
from .models import Action, Task
from django import forms
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, TimePickerInput

class ActionForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(ActionForm, self).clean()
        start = cleaned_data.get('started_at')
        end = cleaned_data.get('ended_at')
        if start > end:
            raise forms.ValidationError({"ended_at": "End date must be higher than start date!"})
        print(start, end)

    class Meta:
        model = Action
        fields =  ['name', 'started_at', 'ended_at']
        widgets = {
            'started_at' : TimePickerInput(),
            'ended_at': TimePickerInput(),
        }

