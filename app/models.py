from django.db import models
from django.db.models import Sum
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
    generation  = models.IntegerField(null=True)
    sex         = models.IntegerField(choices=SEXES_CHOICE, default=1)
    curriculums = models.ManyToManyField(Curriculum, through='Lesson')
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self):
        self.generation = self.calc_generation()
        super(User, self).save()

    def calc_generation(self):
        return math.floor(self.age / 10) * 10

class Lesson(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    time       = models.IntegerField()
    charge     = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self):
        self.charge = self.calc_charge()
        super(Lesson, self).save()

    def calc_charge(self):
        charge = self.curriculum.basic_charge + (self.curriculum.metered_charge * self.time)
        return charge

class Invoice:

    def __init__(self, user, year, month):
        self.user = user
        self.lessons = user.lesson_set.filter(created_at__year = year, created_at__month = month)

    @property
    def curriculum_list(self):
        curriulum_list = []
        for lesson in self.lessons:
            if lesson.curriculum.name not in curriulum_list:
                curriulum_list.append(lesson.curriculum.name)
        return curriulum_list

    @property
    def charge(self):
        if self.lessons.count() != 0:
            return self.lessons.aggregate(Sum('charge'))['charge__sum']
        else:
            return 0
