from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('main.views',
    # Urls to main app
    url(r'^$', 'index', name='index'),
    url(r'^map/?$', 'map', name='map'),
    url(r'^search/?$', 'search', name='search'),
    url(r'^search/get_credits/?$', 'get_credits', name='get_credits'),
    url(r'^graph/?$', 'graph', name='graph'),
    url(r'^login/?$', 'login', name='login'),
    url(r'^logout/?$', 'logout', name='logout'),
    url(r'^manage/?$', 'manage', name='manage'),
    url(r'^change_db/?$', 'change_db', name='change_db'),
    url(r'^get_graph_by_state/?$', 'get_graph_by_state', name='get_graph_by_state'),
    url(r'^get_credits_search/?$', 'get_credits_search', name='get_credits_search'),
    # Urls to django admin
    url(r'^admin/', include(admin.site.urls)),
    # Django registration
    url(r'^accounts/', include('registration.backends.default.urls')),
)

# Static files serve
from django.conf.urls.static import static
from django.conf import settings
import re

urlpatterns += patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), 'django.contrib.staticfiles.views.serve', kwargs={'insecure':True}),
)