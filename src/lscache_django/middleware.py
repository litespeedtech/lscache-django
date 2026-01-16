from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class LSCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.method not in ["GET", "HEAD"]:
            return response

        skip_cookies = getattr(settings, "LSCACHE_SKIP_COOKIES", [])
        if any(cookie in request.COOKIES for cookie in skip_cookies):
            response["X-LiteSpeed-Cache-Control"] = "no-cache"
        elif "X-LiteSpeed-Cache-Control" not in response:
            max_age = getattr(settings, "LSCACHE_DEFAULT_MAX_AGE", None)
            cacheability = getattr(settings, "LSCACHE_DEFAULT_CACHEABILITY", "public")

            if max_age is None or max_age == 0:
                response["X-LiteSpeed-Cache-Control"] = "no-cache"
            else:
                response["X-LiteSpeed-Cache-Control"] = f"max-age={max_age},{cacheability}"

        return response
