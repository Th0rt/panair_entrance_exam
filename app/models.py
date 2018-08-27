import math
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Discount_pattern(models.Model):
    start_total_time = models.IntegerField(
        verbose_name = '適用開始時間'
    )
    discount_per_hour = models.IntegerField(
        verbose_name = '１時間あたりの割引額'
    )
    created_at = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

    def __str__(self):
        return "%sh以上 ¥%s円引" % (self.start_total_time, self.discount_per_hour)

class Curriculum(models.Model):
    name = models.CharField(
        verbose_name = 'カリキュラム名',
        max_length   = 50
    )
    basic_charge = models.IntegerField (
        verbose_name = '基本料金'
    )
    basic_lesson_time = models.IntegerField(
        verbose_name = '基本料金に含まれる時間',
        default      = 0
    )
    metered_charge = models.IntegerField (
        verbose_name = '従量料金'
    )
    discount_pattern = models.ManyToManyField(
        Discount_pattern,
        verbose_name = '割引パターン',
    )
    created_at = models.DateTimeField(
        verbose_name = '作成日',
        default      = timezone.now
    )

    def __str__(self):
        return self.name

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

    def total_lesson_time(self, curriculum_id, year, month):
        total_lesson_time = self.lesson_set.filter(
            curriculum__id       = curriculum_id,
            lesson_date__year    = year,
            lesson_date__month   = month
        ).aggregate(Sum('time'))['time__sum']

        if total_lesson_time is None: total_lesson_time = 0
        return total_lesson_time

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
    lesson_date = models.DateField(
        verbose_name = '受講日',
        default      = timezone.now
    )
    time = models.IntegerField(
        verbose_name = '受講時間(h)',
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
        self.charge = self.total_charge()
        super(Lesson, self).save()

    def total_charge(self):
        return self.basic_charge() + self.metered_charge() - self.discount()

    def basic_charge(self):
        if self.user.total_lesson_time(self.curriculum.id, 2018, 8) == 0:
            return self.curriculum.basic_charge
        else:
            return 0

    def metered_charge(self):
        if self.user.total_lesson_time(self.curriculum.id, 2018, 8) == 0:
            return self.curriculum.metered_charge * (self.time - self.curriculum.basic_lesson_time)
        else:
            return self.curriculum.metered_charge * self.time

    def discount(self):
        patterns            = self.curriculum.discount_pattern.order_by('start_total_time')
        current_lesson_time = self.user.total_lesson_time(self.curriculum.id, 2018, 8)
        add_lesson_time     = self.time
        discount_time       = 0
        discount            = 0

        if patterns.count() == 0: return 0

        for i, pattern in enumerate(patterns):
            discount_range_begin = pattern.start_total_time
            if current_lesson_time < discount_range_begin: continue

            if i == patterns.count() - 1:
                discount_time = add_lesson_time
            else:
                discount_range_end = patterns[i + 1].start_total_time
                if current_lesson_time < discount_range_end:
                    discount_time = min(add_lesson_time, discount_range_end - current_lesson_time)

            current_lesson_time += discount_time
            add_lesson_time   -= discount_time
            discount          += discount_time * pattern.discount_per_hour

            if add_lesson_time <= 0 : break

        return discount

class Invoice:

    def __init__(self, user, year, month):
        self.user = user
        self.lessons = user.lesson_set.filter(lesson_date__year = year, lesson_date__month = month)

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
