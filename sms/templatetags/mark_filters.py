from django import template
from sms.models import Mark

register = template.Library()

@register.filter
def get_mark(student, paper):
    try:
        return Mark.objects.get(student=student, paper=paper).marks_obtained
    except Mark.DoesNotExist:
        return None
    except Exception as e:
        logger.error(f"Error getting mark: {str(e)}")
        return None