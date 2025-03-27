from django import template

register = template.Library()

@register.filter
def getattr(obj, attr):
    """Template filter to get attribute of an object"""
    if hasattr(obj, attr):
        return getattr(obj, attr)
    elif hasattr(obj, 'get'):
        return obj.get(attr, '')
    return ''