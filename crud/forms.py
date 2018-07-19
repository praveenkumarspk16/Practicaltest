from django import forms
from crud.models import Student
from django.core.validators import ValidationError


def checkName(value):
    if value.isdigit():
        raise ValidationError('Name cannot be digit')


class StudentForm(forms.ModelForm):
    email = forms.CharField(
        max_length=20,
        validators=[checkName]
    )
    Address = forms.CharField(
        max_length=250,
        widget=forms.Textarea
    )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
