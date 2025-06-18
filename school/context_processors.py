from django.core.cache import cache
from .models import SchoolConfig


def school_config(request):
    try:
        # Try to get from cache first
        config = cache.get('school_config')
        if not config:
            config = SchoolConfig.load()
            cache.set('school_config', config, 300)  # Cache for 5 minutes

        return {
            'school_config': config,
            'school_info': {  # For backward compatibility
                'name': config.school_name,
                'logo': config.school_logo,
                'motto': config.motto,
                'phone': config.phone,
                'email': config.email,
                'location': config.location
            }
        }
    except Exception as e:
        # Fallback if something goes wrong
        return {
            'school_config': None,
            'school_info': {
                'name': 'School Name',
                'logo': None,
                'motto': 'School Motto',
                # other defaults
            }
        }