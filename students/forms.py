from django import forms
from home.models import Courses

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Courses.objects.all(),
                                    widget=forms.HiddenInput)