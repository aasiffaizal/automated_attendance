# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Classroom, Timetable, Subject
admin.site.register(Classroom)
admin.site.register(Timetable)
admin.site.register(Subject)
