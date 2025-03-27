from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def percentage(value, total):
    """Calculate percentage of value from total"""
    try:
        return round((float(value) / float(total)) * 100)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def sum_papers(subjects):
    """Sum all papers for given subjects queryset"""
    return sum(subject.papers.count() for subject in subjects)

@register.filter(name='abs')
def absolute_value(value):
    """Return absolute value"""
    return abs(value)

@register.filter
@stringfilter
def truncatechars(value, arg):
    """Truncate a string after arg number of characters"""
    try:
        length = int(arg)
    except ValueError:
        return value
    if len(value) > length:
        return value[:length] + '...'
    return value