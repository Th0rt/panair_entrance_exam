import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Sum, Count
from .models import User, Lesson, Curriculum, Invoice
from .forms import UserForm, LessonForm


def index(request):
    year = datetime.datetime.now().strftime('%Y')
    month = datetime.datetime.now().strftime('%m')
    return render(request, 'app/index.html', {'year': year, 'month': month})

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

def invoices_index(request, year, month):
    invoices = [ Invoice(user, year, month) for user in User.objects.all() ]
    return render(request, 'app/invoices/index.html', {'invoices': invoices })

def reports_index(request, year, month):
    report_by_sex = []

    for curriculum in Curriculum.objects.all():
        for i in [1,2]:
            reportline = {
                'curriculum__name' : curriculum.name,
                'user__sex': i
            }
            reportline.update(
                Lesson.objects.filter(
                    curriculum__name = curriculum.name,
                    user__sex = i
                ).aggregate(
                    Count('id'),
                    Count('user', distinct = True),
                    Sum('charge'),
                )
            )
            report_by_sex.append(reportline)

    report_by_generation = []
    for curriculum in Curriculum.objects.all():
        for i in [1,2]:
            for generation in [10, 20, 30, 40, 50, 60, 70, 80]:
                reportline = {
                    'curriculum__name' : curriculum.name,
                    'user__sex': i,
                    'user__generation': generation,
                }
                reportline.update(
                    Lesson.objects.filter(
                        curriculum__name = curriculum.name,
                        user__sex = i,
                        user__generation = generation,
                    ).aggregate(
                        Count('id'),
                        Count('user', distinct = True),
                        Sum('charge'),
                    )
                )
                report_by_generation.append(reportline)
    return render(request, 'app/reports/index.html',
                  { 'report_by_sex': report_by_sex,
                    'report_by_generation': report_by_generation })

