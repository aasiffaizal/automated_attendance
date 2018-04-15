from django import template
from datetime import datetime
from timetable.models import Classroom
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter()
def to_float(attendance):
    return float(attendance)
@register.filter()
def round(attendance):
    return ('%f' % float(attendance)).rstrip('0').rstrip('.')

@register.filter()
def get_type(value):
    if type(value)==str:
        return('str')
    elif type(value)==int:
        return('int')
    elif type(value)==float:
        return('float')

@register.filter()
@stringfilter
def change_dateformat(value):
    date=value.replace(',','')
    #date = datetime.strptime(date, '%B %d %Y').strftime('%Y-%m-%d')
    return date

@register.filter()
def slug(value):
    Class=Classroom.objects.get(class_id=value)
    slug=Class.slug
    return slug