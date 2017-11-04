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
class ProfileFor(forms.ModelForm):
	username = forms.CharField(label = 'dd')
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.name = self.user.username
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['username'] = forms.CharField(label = 'Username',initial = self.name, disabled = 'disabled')

	class Meta:
		model = NotificationTime
		fields = ('Notification_time',)

	def save(self, commit=True):
		obj = Personnel.objects.get(LDAP_id=self.user.id)
		personID = obj.Person_ID
		personObj = Personnel.objects.get(Person_ID=personID)
		obj_ , created = NotificationTime.objects.update_or_create(Personnel_ID=personObj,defaults={'Notification_time':self.cleaned_data.get('Notification_time')})
		return obj_
