from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from .models import Lesson
from .forms import UserForm, LessonForm


def index(request):
    return render(request, 'app/index.html', {})


def users_index(request):
    users = User.objects.all()
    return render(request, 'app/users/index.html', {'users': users})

def user_edit(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        edit_user = UserForm(request.POST, instance=user)
        if edit_user.is_valid():
            edit_user.save()
            return redirect('app:users')
    else:
        form = UserForm(instance=user)
    return render(request, 'app/users/new.html', {'form': form})

def user_new(request):
    if request.method == 'POST':
        new_user = UserForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            return redirect('app:users')
    else:
        form = UserForm()
    return render(request, 'app/users/new.html', {'form': form})

def lessons_index(request):
    lessons = Lesson.objects.all()
    return render(request, 'app/lessons/index.html', {'lessons': lessons})

def lessons_new(request):
    if request.method == 'POST':
        new_lesson = LessonForm(request.POST)
        if new_lesson.is_valid():
            new_lesson.save()
            return redirect('app:lessons')
    else:
        form = LessonForm()
    return render(request, 'app/lessons/edit.html', { 'form' : form })

def lessons_edit(request, id):
    lesson = Lesson.objects.get(id=id)
    if request.method == 'POST':
        edit_lesson = LessonForm(request.POST, instance = lesson)
        if edit_lesson.is_valid():
            edit_lesson.save()
            return redirect('app:lessons')
    else:
        form = LessonForm(instance = lesson)
    return render(request, 'app/lessons/edit.html', { 'form': form })

def invoices_index(request):
    return render(request, 'app/invoices/index.html')
