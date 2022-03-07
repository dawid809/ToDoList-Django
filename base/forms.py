from argparse import Action
from django import forms


class AddForm(forms.ModelForm):
    model = Action
    fields = '__all__'
    
