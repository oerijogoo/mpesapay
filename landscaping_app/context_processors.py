# landscaping_app/context_processors.py

from .models import BusinessSettings

def business_settings(request):
    try:
        settings = BusinessSettings.objects.first()
    except BusinessSettings.DoesNotExist:
        settings = None
    return {'business_settings': settings}