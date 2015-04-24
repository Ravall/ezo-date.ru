from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from solar.views import index, sopen, days12, day

urlpatterns = patterns('',
    url(r'^$', index.IndexView.as_view(), name='solar_home'),
    url(r'^open/(?P<city_id>\d+)/(?P<date>\d{12})/(?P<year>\d{4})$', sopen.OpenView.as_view(), name='solar_open'),
    url(r'^12days$', days12.List.as_view(), name='solar_12_days'),
    url(r'^day/(?P<nday>\d+)$', day.Show.as_view(), name='solar_day'),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
