from django.shortcuts import render
from .models import User


def index(request):
    return render(request, 'app/index.html', {})


def users_index(request):
    users = User.objects.all()
    return render(request, 'app/users/index.html', {'users': users})

def users_show(request, id):
    user = User.objects.get(id=id)
    return render(request, 'app/users/show.html', {'user': user})
