from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from .forms import UserForm


def index(request):
    return render(request, 'app/index.html', {})


def users_index(request):
    users = User.objects.all()
    return render(request, 'app/users/index.html', {'users': users})

def user_show(request, id):
    user = User.objects.get(id=id)
    return render(request, 'app/users/show.html', {'user': user})

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
    return render(request, 'app/lessons/index.html')

def lessons_new(request):
    return render(request, 'app/lessons/edit.html')

def lessons_edit(request, id):
    return render(request, 'app/lessons/edit.html')

def invoices_index(request):
    return render(request, 'app/invoices/index.html')
