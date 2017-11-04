from django import forms
from models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import json

class PersonnelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Personnel
        fields = ('Person_ID','Role','Dept')

#Form for taking input from user for email frequency

