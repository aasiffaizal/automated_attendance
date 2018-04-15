# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-26 04:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0006_auto_20180225_1923'),
        ('login', '0002_students'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Students')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.Subject')),
            ],
        ),
    ]
