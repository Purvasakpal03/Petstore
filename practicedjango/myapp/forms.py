from django import forms
from .models import Taskapp

class createform(forms.ModelForm):
    class Meta:
        model = Taskapp
        fields = ['name','description','status']