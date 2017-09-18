# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from frontend.views import Index
from user.views import AjaxCity



admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='home'),


    url(r'^numerology/', include('numerology.urls')),
    url(r'^biorythms/', include('biorythms.urls')),
    url(r'^moonbirthday/', include('moonbirthday.urls')),
    url(r'^solar/', include('solar.urls')),
    url(r'^moonphases/', include('moonphases.urls')),
    url(r'^suntime/', include('suntime.urls')),


    url(r'', include('robots_txt.urls')),
    url(r'^', include('favicon.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^geoip/', include('django_geoip.urls')),


    url(r'^ajax/city/$', AjaxCity.as_view(), name='ajax_city_autocomplete'),


    url(r'^user/', include('user.reg_urls')),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns