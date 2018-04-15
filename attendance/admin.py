# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Record,Counting,Record1,Error
admin.site.register(Record)
admin.site.register(Counting)
admin.site.register(Record1)
admin.site.register(Error)