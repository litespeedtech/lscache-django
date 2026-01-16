from .decorators import lscache
from .middleware import LSCacheMiddleware
from .purging import lscache_purge

default_app_config = "lscache_django.apps.DjangoLSCacheConfig"