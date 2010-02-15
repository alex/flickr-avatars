import os
import urllib

from django.conf import settings

settings.configure(
    CACHE_BACKEND="locmem://",
    TEMPLATE_DIRS=[
        os.path.join(os.path.dirname(__file__), "templates")
    ],
)

from django.core.cache import cache
from django.conf.urls.defaults import patterns, url
from django.http import Http404, HttpResponseRedirect

from pyquery import PyQuery

from django_wsgi import wsgi_application


FLICKR_PROFILE_URL = "http://www.flickr.com/photos/%s/"
FLICKR_AVATAR_URL = "http://www.flickr.com/buddyicons/%s.jpg"

def avatar(request, username):
    cache_key = "flickr:uid:%s" % username
    uid = cache.get(cache_key)
    if uid is None:
        page = urllib.urlopen(FLICKR_PROFILE_URL % username)
        if page.getcode() != 200:
            raise Http404
        page = PyQuery(page.read())
        uid = page.find("input[name=w]").val()
        cache.set(cache_key, uid)
    return HttpResponseRedirect(FLICKR_AVATAR_URL % uid)


urlpatterns = patterns("",
    url(r"^$", "django.views.generic.simple.direct_to_template",
        {"template": "home.html"}),
    url(r"^i/(?P<username>.*?)\.jpg", avatar),
    url(r"^static/(?P<path>.*)$", "django.views.static.serve",
        {"document_root": os.path.join(os.path.dirname(__file__), "static")})
)

application = wsgi_application(urlpatterns)
