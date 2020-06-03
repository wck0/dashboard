from django import forms
from django.core import validators

class StudentsForm(forms.Form):
    file = forms.FileField()


