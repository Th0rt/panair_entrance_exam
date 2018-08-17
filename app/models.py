from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
