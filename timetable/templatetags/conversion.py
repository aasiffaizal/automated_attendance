from django import template
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