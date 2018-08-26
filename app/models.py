import math
from django.db import models
from django.db.models import Sum
from django.utils import timezone

class Curriculum(models.Model):
    name = models.CharField(
        verbose_name = 'カリキュラム名',
        max_length   = 50
    )
    basic_charge = models.IntegerField (
        verbose_name = '基本料金'
    )
    metered_charge = models.IntegerField (
        verbose_name = '従量料金'
    )
    created_at = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

    def __str__(self):
        return self.name

class Discount_pattern(models.Model):
    start_total_time = models.IntegerField(
        verbose_name = '適用開始時間'
    )
    discount_per_hour = models.IntegerField(
        verbose_name = '１時間あたりの割引額'
    )
    curriculums = models.ManyToManyField(
        Curriculum,
        verbose_name = '適用するカリキュラム',
    )
    created_at = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

class User(models.Model):
    name = models.CharField(
        verbose_name = 'ユーザー名',
        max_length   = 50
    )
    age = models.IntegerField(
        verbose_name = '年齢'
    )
    generation  = models.IntegerField(
        verbose_name = '年代',
        null         = True
    )
    sex = models.IntegerField(
        verbose_name = '性別',
        choices      = ((1, '男性'), (2, '女性')),
        default      = 1
    )
    curriculums = models.ManyToManyField(
        Curriculum,
        through      = 'Lesson',
        verbose_name = '受講記録'
    )
    created_at  = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

    def __str__(self):
        return self.name

    def save(self):
        self.generation = self.calc_generation()
        super(User, self).save()

    def calc_generation(self):
        return math.floor(self.age / 10) * 10

class Lesson(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name = 'ユーザー',
        on_delete    = models.CASCADE
    )
    curriculum = models.ForeignKey(
        Curriculum,
        verbose_name = 'カリキュラム',
        on_delete    = models.CASCADE
    )
    time = models.IntegerField(
        verbose_name = '受講時間(h)'
    )
    charge = models.IntegerField(
        verbose_name = '料金',
        null         = True
    )
    created_at = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

    def save(self):
        self.charge = self.calc_charge()
        super(Lesson, self).save()

    def calc_charge(self):
        charge = self.curriculum.basic_charge + (self.curriculum.metered_charge * self.time)
        discount = self.calc_discount()
        return (charge - discount)

    def calc_discount(self):
        patterns    = self.curriculum.discount_pattern_set.order_by('-start_total_time')
        lesson_time = self.time
        discount    = 0

        if patterns.count() == 0: return 0

        for pattern in patterns:
            if self.time > pattern.start_total_time:
                discount += (lesson_time - pattern.start_total_time) * pattern.discount_per_hour
                lesson_time = pattern.start_total_time
        return discount

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
