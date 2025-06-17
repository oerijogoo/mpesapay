from django import template

register = template.Library()

@register.filter
def find_report(reports, student):
    return reports.filter(student=student).first()