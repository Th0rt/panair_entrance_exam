# Generated by Django 2.1 on 2018-08-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20180827_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount_pattern',
            name='curriculums',
        ),
        migrations.AddField(
            model_name='curriculum',
            name='discount_pattern',
            field=models.ManyToManyField(to='app.Discount_pattern', verbose_name='割引パターン'),
        ),
    ]