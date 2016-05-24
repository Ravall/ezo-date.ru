from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from solar.views import IndexView, Days12View, DayView, FormView, OpenView
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='solar_home'),
    url(r'^open$', OpenView.as_view(), name='solar_open'),
    url(r'^open/(?P<year>\d+)$$', OpenView.as_view(), name='solar_open_year'),
    url(r'^12days$', Days12View.as_view(), name='solar_12'),
    url(r'^day/(?P<nday>\d+)$', DayView.as_view(), name='solar_day'),
    url(r'^form$', FormView.as_view(), name='solar_form'),

    url(r'^open/\d+/\d{12}/\d{4}$',  RedirectView.as_view(pattern_name='solar_open', permanent=True)),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
