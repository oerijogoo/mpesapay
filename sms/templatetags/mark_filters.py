# sms/templatetags/mark_filters.py
from django import template
from ..models import Mark

register = template.Library()

@register.filter
def get_mark(student, paper):
    try:
        return Mark.objects.get(student=student, paper=paper).marks_obtained
    except Mark.DoesNotExist:
        return None