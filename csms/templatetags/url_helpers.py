from django import template

register = template.Library()

@register.filter
def to_url_name(value):
    """Converts 'Academic Year' to 'academicyear' for URL names"""
    return value.lower().replace(' ', '')