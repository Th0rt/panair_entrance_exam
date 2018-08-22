from django.contrib import admin
from .models import User
from .models import Curriculum
from .models import Lesson

admin.site.register(User)
admin.site.register(Curriculum)
admin.site.register(Lesson)
