from functools import wraps
from django.conf import settings

def lscache(max_age=None, cacheability=None, esi=False, tags=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if max_age == 0 or cacheability == "no-cache":
                response["X-LiteSpeed-Cache-Control"] = "no-cache"
                return response

            _max_age = (
                max_age
                if max_age is not None
                else getattr(settings, "LSCACHE_DEFAULT_MAX_AGE", None)
            )
            _cacheability = (
                cacheability
                if cacheability is not None
                else getattr(settings, "LSCACHE_DEFAULT_CACHEABILITY", None)
            )

            if _max_age is not None and _cacheability:
                header = f"max-age={_max_age},{_cacheability}"
                if esi:
                    header += ",esi=on"
                response["X-LiteSpeed-Cache-Control"] = header

            if tags:
                if isinstance(tags, (list, tuple)):
                    response["X-LiteSpeed-Tag"] = ",".join(tags)
                else:
                    response["X-LiteSpeed-Tag"] = str(tags)

            return response

        return wrapper
    return decorator
