from django import forms
from .models import User, Lesson

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'sex', 'age')

class LessonForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = ('user', 'curriculum', 'time')
