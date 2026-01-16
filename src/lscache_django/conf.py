from django.conf import settings

def apply_defaults():
    defaults = {
        "LSCACHE_SKIP_COOKIES": ["sessionid"],
        "LSCACHE_DEFAULT_MAX_AGE": 60,
        "LSCACHE_DEFAULT_CACHEABILITY": "public",
        "LSCACHE_ESI_ENABLED": False,
    }

    for key, value in defaults.items():
        if not hasattr(settings, key):
            setattr(settings, key, value)
