# Generated by Django 2.1 on 2018-08-26 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_discount_pattern'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculum',
            name='basic_lesson_time',
            field=models.IntegerField(default=0),
        ),
    ]
