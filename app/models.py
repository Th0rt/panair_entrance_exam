from django.db import models
from django.utils import timezone

class Curriculum(models.Model):
    name           = models.CharField(max_length=50)
    basic_charge   = models.IntegerField()
    metered_charge = models.IntegerField()
    created_at     = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class User(models.Model):
    SEXES_CHOICE = ((1, '男性'), (2, '女性'))
    name       = models.CharField(max_length=50)
    age        = models.IntegerField()
    sex        = models.IntegerField(choices=SEXES_CHOICE, default=1)
    lessons    = models.ManyToManyField(Curriculum, through='Lesson')
    created_at = models.DateTimeField(default=timezone.now)

class Lesson(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    time       = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def metered_charge(self):
        return self.curriculum.metered_charge * self.time

    def total_charge(self):
        return self.curriculum.basic_charge + self.metered_charge()
