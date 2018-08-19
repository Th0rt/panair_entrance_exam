from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from .forms import UserForm


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
