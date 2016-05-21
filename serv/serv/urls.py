from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from frontend.views import Index
from django.views.generic import TemplateView
from django.views.defaults import page_not_found, server_error
from serv.sitemap import site_map
from frontend.v2 import V2


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='home'),
    url(r'^v2$', V2.as_view(), name='v2'),


    url(r'^numerology/', include('numerology.urls')),
    url(r'^biorythms/', include('biorythms.urls')),
    url(r'^moonbirthday/', include('moonbirthday.urls')),
    url(r'^solar/', include('solar.urls')),
    url(r'^moonphases/', include('moonphases.urls')),
    url(r'^suntime/', include('suntime.urls')),


    url(r'', include('robots_txt.urls')),
    url(r'^', include('favicon.urls')),

    url(r'^sitemap\.xml$', site_map),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^geoip/', include('django_geoip.urls')),

#    url(r'^404/$', page_not_found),
#    url(r'^500/$', server_error)

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
