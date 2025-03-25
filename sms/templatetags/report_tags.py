from django import template

register = template.Library()

@register.filter
def sum_attr(items, attr_name):
    """Sum a specific attribute from a list of objects"""
    return sum(getattr(item, attr_name, 0) for item in items)