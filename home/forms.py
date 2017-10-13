from django import forms
from models import *

class PersonnelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Personnel
        fields = ('Person_ID','Role','Dept')
