# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-27 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0013_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='error_hrs',
            field=models.CharField(max_length=15),
        ),
    ]
