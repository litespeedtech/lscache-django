from django.test import RequestFactory, TestCase
from django.http import HttpResponse
from lscache_django.decorators import lscache
from lscache_django.middleware import LSCacheMiddleware
import unittest

####### To run test_lscache.py for app ######
### mkdir -p app/tests && touch app/tests/__init__.py 
### curl -o app/tests/test_lscache.py https://raw.githubusercontent.com/litespeedtech/lscache-django/main/tests/test_lscache.py
### python manage.py test app

class LSCacheMiddlewareTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = LSCacheMiddleware(lambda request: HttpResponse())

    def _get_response(self, request, response):
        return self.middleware.process_response(request, response)

    def test_public_cache_header(self):
        @lscache(max_age=120)
        def view(request):
            return HttpResponse("Hello World")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)
        actual = response["X-LiteSpeed-Cache-Control"]
        expected = "max-age=120,public"
        print(f"[TEST] test_public_cache_header | Expected: {expected}, Actual: {actual}")
        self.assertEqual(actual, expected)

    def test_no_cache(self):
        @lscache(max_age=0)
        def view(request):
            return HttpResponse("No cache")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)
        actual = response["X-LiteSpeed-Cache-Control"]
        expected = "no-cache"
        print(f"[TEST] test_no_cache | Expected: {expected}, Actual: {actual}")
        self.assertEqual(actual, expected)

    def test_private_cache(self):
        @lscache(max_age=180, cacheability="private")
        def view(request):
            return HttpResponse("Private")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)
        actual = response["X-LiteSpeed-Cache-Control"]
        expected = "max-age=180,private"
        print(f"[TEST] test_private_cache | Expected: {expected}, Actual: {actual}")
        self.assertEqual(actual, expected)

    def test_cache_tags(self):
        @lscache(max_age=120, tags=["blog", "frontpage"])
        def view(request):
            return HttpResponse("Tagged")

        request = self.factory.get("/")
        response = view(request)
        response = self._get_response(request, response)
        actual = response["X-LiteSpeed-Tag"]
        expected = "blog,frontpage"
        print(f"[TEST] test_cache_tags | Expected: {expected}, Actual: {actual}")
        self.assertEqual(actual, expected)

    def test_admin_is_no_cache(self):
        @lscache(max_age=0)
        def admin_view(request):
            return HttpResponse("admin")

        request = self.factory.get("/admin/")
        response = admin_view(request)
        response = self.middleware.process_response(request, response)
        actual = response["X-LiteSpeed-Cache-Control"]
        expected = "no-cache"
        print(f"[TEST] test_admin_is_no_cache | Expected: {expected}, Actual: {actual}")
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(LSCacheMiddlewareTest)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n===== TEST SUMMARY =====")
    print(f"Total tests   : {result.testsRun}")
    print(f"Passed        : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures      : {len(result.failures)}")
    print(f"Errors        : {len(result.errors)}")
