from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_attr')
def get_attr(obj, attr):
    """Template filter to get an attribute from an object dynamically"""
    try:
        value = getattr(obj, attr)
        if callable(value):
            value = value()
        return value
    except AttributeError:
        return ''