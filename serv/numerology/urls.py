from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from numerology.views import IndexView, NumerologyFormView, AllNumsView, NumView, NumerologyResult

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='num_home'),
    url(r'^form$', NumerologyFormView.as_view(), name='num_form'),
    url(r'^result$', NumerologyResult.as_view(permanent=False), name='num_result'),
    url(r'(?P<digit>[0-9]+)', NumView.as_view(), name='num_birthday'),
    url(r'^all$', AllNumsView.as_view(), name='all_nums'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
