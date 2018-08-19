from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('',                    views.index,       name='index'),
    path('users',               views.users_index, name='users'),
    path('users/<int:id>/edit', views.user_edit,   name='user_edit'),
    path('users/new',           views.user_new,    name='user_new'),
]
