# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Staff,Students


admin.site.register(Staff)
admin.site.register(Students)
