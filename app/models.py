import math, datetime
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from dateutil.relativedelta import relativedelta
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

    @property
    def discount_pattern_list(self):
        discount_patterns = self.discount_pattern.order_by('start_total_time')
        discount_pattern_list = []

        for i, discount_pattern in enumerate(discount_patterns):
            pattern = {
                'value'            : discount_pattern.discount_per_hour,
                'lesson_time_begin': discount_pattern.start_total_time
            }
            if discount_pattern != discount_patterns.last():
                pattern['lesson_time_end'] = discount_patterns[i + 1].start_total_time

            discount_pattern_list.append(pattern)

        return discount_pattern_list

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

    def total_lesson_time(self, **kwargs):
        lessons = self.lesson_set.filter(**kwargs)
        return sum([ lesson.time for lesson in lessons ])

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
        validators   = [
            MinValueValidator(1),
            MaxValueValidator(12)
        ]
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
        self.charge = self.total_charge
        super(Lesson, self).save()

    @property
    def total_charge(self):
        return self.basic_charge + self.metered_charge - self.discount

    @property
    def basic_charge(self):
        total_lesson_time_exclude_this = self.user.total_lesson_time(
            curriculum__id = self.curriculum.id,
            lesson_date__range = (
                self.lesson_date - relativedelta(days = self.lesson_date.day - 1),
                self.lesson_date - relativedelta(days = 1)
            )
        )
        if total_lesson_time_exclude_this <= 0:
            return self.curriculum.basic_charge
        else:
            return 0

    @property
    def metered_charge(self):
        total_lesson_time_exclude_this = self.user.total_lesson_time(
            curriculum__id     = self.curriculum.id,
            lesson_date__range = (
                self.lesson_date - relativedelta(days = self.lesson_date.day - 1),
                self.lesson_date - relativedelta(days = 1)
            )
        )
        if total_lesson_time_exclude_this < self.curriculum.basic_lesson_time:
            return self.curriculum.metered_charge * max(total_lesson_time_exclude_this + self.time - self.curriculum.basic_lesson_time, 0)
        else:
            return self.curriculum.metered_charge * self.time

    @property
    def discount(self):
        return sum([ discount['discount_value'] for discount in self.discount_detail ])

    @property
    def discount_detail(self):
        discount_patterns   = self.curriculum.discount_pattern_list
        total_lesson_time_exclude_this = self.user.total_lesson_time(
            curriculum__id = self.curriculum.id,
            lesson_date__range = (
                self.lesson_date - relativedelta(days = self.lesson_date.day - 1),
                self.lesson_date - relativedelta(days = 1)
            )
        )
        total_lesson_time_include_this = total_lesson_time_exclude_this + self.time

        for pattern in discount_patterns:
            if 'lesson_time_end' in pattern:
                discount_range    = range(pattern['lesson_time_begin'] + 1, pattern['lesson_time_end'] + 1)
                lesson_time_range = range(total_lesson_time_exclude_this + 1, total_lesson_time_include_this + 1)
                discount_hour = len([ i for i in lesson_time_range if i in discount_range ])
            else:
                discount_hour = total_lesson_time_include_this - pattern['lesson_time_begin']

            pattern['discount_hour']  = max(discount_hour, 0)
            pattern['discount_value'] = pattern['discount_hour'] * pattern['value']

        return discount_patterns

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
        return sum([ lesson.total_charge for lesson in self.lessons ])

class Report:
    lessons = []

    def __init__(self, **kwargs):
        self.lessons = [ lesson for lesson in Lesson.objects.filter(**kwargs) ]

    @property
    def lessons_count(self):
        return len(self.lessons)

    @property
    def curriculums(self):
        return list(set([ lesson.curriculum for lesson in self.lessons ]))

    @property
    def users(self):
        return list(set([ lesson.user for lesson in self.lessons ]))

    @property
    def users_count(self):
        return len(self.users)

    @property
    def sum_charge(self):
        return sum([ lesson.total_charge for lesson in self.lessons ])
