from .models import SchoolConfig


def school_config(request):
    try:
        config = SchoolConfig.objects.first()
    except:
        config = None

    return {
        'school_config': config
    }