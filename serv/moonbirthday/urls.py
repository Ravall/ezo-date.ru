from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from moonbirthday.views import IndexView, NumsView, OneNumView, FormView, MyDayView
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='moonbirthday_home'),
    url(r'^nums$', NumsView.as_view(), name='moonbirthday_nums'),
    url(r'^(?P<nday>[0-9]+)_lunnyy_den_rozhdeniya/$', OneNumView.as_view(), name='moonbirthday_one_num'),
    url(r'^form$', FormView.as_view(), name='moonbirthday_form'),
    url(r'^my$', MyDayView.as_view(), name='moonbirthday_my_day'),
    
    url(r'^all$', RedirectView.as_view(pattern_name='moonbirthday_nums', permanent=True))
    
    
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
