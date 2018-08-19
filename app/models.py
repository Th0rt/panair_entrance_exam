from django.db import models
from django.utils import timezone


class User(models.Model):
    SEXES_CHOICE = ((1, '男性'), (2, '女性'))
    name       = models.CharField(max_length=50)
    age        = models.IntegerField()
    sex        = models.IntegerField(choices=SEXES_CHOICE, default=1)
    created_at = models.DateTimeField(default=timezone.now)
