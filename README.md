# lscache-django

A simple **LiteSpeed Cache** integration for Django applications.

## Prerequisite

* Running your Django app on LiteSpeed/OpenLiteSpeed Web Server
* Ensure LiteSpeed cache is enabled and the cache folder is writable.

## Installation
```
pip install lscache-django
```

Add `lscache_django` to your `INSTALLED_APPS` in **settings.py**:
```
INSTALLED_APPS = [
    ...
    'lscache_django',
]
```
Add the middleware:
```
MIDDLEWARE = [
    ...
    'lscache_django.middleware.LSCacheMiddleware',
]
```

## Usage
Use the `@lscache` decorator in your views to cache responses. You can control cache duration, cache type, and tags.

```
from lscache_django.decorators import lscache
from django.http import HttpResponse
```

### cache-control

**Admin page (no cache)**

Admin pages should never be cached.
```
@lscache(max_age=0)
def admin_page(request):
    return HttpResponse("Admin page – never cached")
```

This results in:
* x-litespeed-cache-control: no-cache
* No cache entry created

**Public page (/about-us) – cached publicly**

A normal public page cached for 1 hour.
```
@lscache(max_age=3600)
def about_us(request):
    return HttpResponse("About Us – public cache for 1 hour")
```

Result:
* Public cache
* Cached for 3600 seconds

**Blog page – public cache with tags**

Tags allow selective purging later.
```
@lscache(max_age=300, tags=["blog", "frontpage"])
def blog_index(request):
    return HttpResponse("Blog page – cached with tags")
```

Result:
* Public cache
* Tagged with blog and frontpage
* Can be purged by tag without affecting other pages

Contact page – private cache (no tags)

**Private pages are cached per user and usually don’t need tags.**
```
@lscache(max_age=180, cacheability="private")
def contact(request):
    return HttpResponse("Contact page – private cache, no tags")
```

Result:
* Private cache


### Purge Cache
Cache purging is done by sending an X-LiteSpeed-Purge response header.

Add the helper and the following examples in your app views:
```
from lscache_django import lscache_purge
from django.http import HttpResponse
```

**Purge by tag**

This is the most common and safest way to purge.
```
def purge_blog(request):
    response = HttpResponse("Blog cache purged")
    response["X-LiteSpeed-Purge"] = lscache_purge(
        tags=["blog", "frontpage"],
        stale=True
    )
    return response
```

This purges all cached pages with those tags.


**Purge specific URLs (items)**

You can also purge individual paths.
```
def purge_about_us(request):
    response = HttpResponse("About Us cache purged")
    response["X-LiteSpeed-Purge"] = lscache_purge(
        uris=["/about-us/"],
        stale=True
    )
    return response
```

**Purge everything (global purge)**
```
def purge_all(request):
    response = HttpResponse("All cache purged")
    response["X-LiteSpeed-Purge"] = "*"
    return response
```

This clears all public cache entries for the site.


#### Why stale purge matters

By default, LiteSpeed Cache purges an item and regenerates it on the next request.

This works well for low-traffic sites, but consider this scenario:

Page generation time: 2 seconds

50 users hit the page right after a purge

Without stale handling:

* All 50 requests hit Django

* Backend load spikes

* PHP/Django workers get overwhelmed

How stale purge solves this

When using `stale=on`:

* First request regenerates the cache
* Other visitors temporarily receive the stale cached version
* Once regeneration finishes, everyone gets the fresh cache

Because page generation is usually fast, stale content is only served for a very short time, often just a couple of seconds.

This is why stale purge is enabled by default in LiteSpeed.

**Disabling stale purge**

If your application cannot tolerate stale content at all, you can disable it:
```
response["X-LiteSpeed-Purge"] = lscache_purge(
    tags=["blog"],
    stale=False
)
```
This forces all visitors to wait for fresh content after a purge.

### Restart Python Process
LiteSpeed/OpenLiteSpeed comes with python in detached mode by default, so you will need to restart python with following command to make any new settings take effect:
```
killall lswsgi
```