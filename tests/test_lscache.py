from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from lscache_django.decorators import lscache
from lscache_django.middleware import LSCacheMiddleware

class LSCacheMiddlewareTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LSCacheMiddleware()

    def _get_response(self, request, response):
        return self.middleware.process_response(request, response)

    def test_public_cache_header(self):
        @lscache(max_age=120)
        def view(request):
            return HttpResponse("Hello World")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)

        self.assertEqual(
            response["X-LiteSpeed-Cache-Control"],
            "max-age=120,public"
        )

    def test_no_cache(self):
        @lscache(max_age=0)
        def view(request):
            return HttpResponse("No cache")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)

        self.assertEqual(
            response["X-LiteSpeed-Cache-Control"],
            "no-cache"
        )

    def test_private_cache(self):
        @lscache(max_age=180, cacheability="private")
        def view(request):
            return HttpResponse("Private")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)

        self.assertEqual(
            response["X-LiteSpeed-Cache-Control"],
            "max-age=180,private"
        )

    def test_cache_tags(self):
        @lscache(max_age=120, tags=["blog", "frontpage"])
        def view(request):
            return HttpResponse("Tagged")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)

        self.assertEqual(
            response["X-LiteSpeed-Tag"],
            "blog,frontpage"
        )
