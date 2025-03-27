from .models import SchoolSettings

def school_settings(request):
    return {
        'SchoolSettings': SchoolSettings
    }