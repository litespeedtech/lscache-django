from django.apps import AppConfig

class DjangoLSCacheConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lscache_django"
    verbose_name = "LiteSpeed Cache"

    def ready(self):
        from .conf import apply_defaults
        apply_defaults()
