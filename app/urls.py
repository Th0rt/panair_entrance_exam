from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('',               views.index,         name='index'),

    path('users',          views.users_index,   name='users'),
    path('users/<int:id>', views.user_edit,     name='user_edit'),
    path('users/new',      views.user_new,      name='user_new'),

    path('lessons',          views.lessons_index, name='lessons'),
    path('lessons/new',      views.lessons_new,   name='lessons_new'),
    path('lessons/<int:id>', views.lessons_edit,  name='lessons_edit'),

    path('invoices/<int:year>/<int:month>', views.invoices_index, name='invoices')
]
