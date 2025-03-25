from django import template

register = template.Library()

@register.filter
def map_attr(values, attr):
    return [getattr(item, attr) for item in values]