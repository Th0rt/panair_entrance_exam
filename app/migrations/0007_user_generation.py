# Generated by Django 2.1 on 2018-08-24 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_lesson_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='generation',
            field=models.IntegerField(null=True),
        ),
    ]
