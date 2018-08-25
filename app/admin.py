from django.contrib import admin
from .models import User, Curriculum, Lesson, Discount_pattern

admin.site.register(User)
admin.site.register(Curriculum)
admin.site.register(Lesson)
admin.site.register(Discount_pattern)
