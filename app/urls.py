from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('',               views.index,         name='index'),

    path('users',          views.users_index,   name='users'),
    path('users/<int:id>', views.user_show,     name='user_show'),
    path('users/new',      views.user_new,      name='user_new'),

    path('lessons',        views.lessons_index, name='lessons')
]
