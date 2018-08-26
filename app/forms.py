from django import forms
from django.forms import DateInput
from .models import User, Lesson

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'sex', 'age')

class LessonForm(forms.ModelForm):

    class Meta:
        model   = Lesson
        fields  = ('user', 'curriculum', 'lesson_date', 'time')
        widgets = {
            'lesson_date' : DateInput(attrs = { "type": "date" })
        }
