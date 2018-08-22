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
    name        = models.CharField(max_length=50)
    age         = models.IntegerField()
    sex         = models.IntegerField(choices=SEXES_CHOICE, default=1)
    curriculums = models.ManyToManyField(Curriculum, through='Lesson')
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    time       = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def metered_charge(self):
        return self.curriculum.metered_charge * self.time

    def total_charge(self):
        return self.curriculum.basic_charge + self.metered_charge()

class Invoice:

    def __init__(self, user, year, month):
        self.user = user
        self.lessons = user.lesson_set.filter(created_at__year = year, created_at__month = month)
        self.charge = sum([lesson.total_charge() for lesson in self.lessons])

    @property
    def curriculum_list(self):
        curriulum_list = []
        for lesson in self.lessons:
            if lesson.curriculum.name not in curriulum_list:
                curriulum_list.append(lesson.curriculum.name)
        return curriulum_list

