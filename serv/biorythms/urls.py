from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from datetime import date
from biorythms.views import IndexView, BioFormView, BioResult, AjaxGetData

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='bio_home'),
    url(r'^form$', BioFormView.as_view(), name='bio_form'),
    url(r'^result$', BioResult.as_view(), name='bio_result'),
    url(r'^ajax/get_bio_data$', AjaxGetData.as_view(), name='ajax_get_data'),
    )

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
