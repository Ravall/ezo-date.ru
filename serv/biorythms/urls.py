from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from datetime import date
from biorythms.views import IndexView, BioFormView, BioResult, AjaxGetData, ArticlesView, ArticleView
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='bio_home'),
    url(r'^form$', BioFormView.as_view(), name='bio_form'),
    url(r'^result$', BioResult.as_view(), name='bio_result'),
    url(r'^ajax/get_bio_data$', AjaxGetData.as_view(), name='ajax_get_data'),

    url(r'^\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}$', RedirectView.as_view(pattern_name='bio_result', permanent=True)),
    url(r'^\d{4}-\d{2}-\d{2}$', RedirectView.as_view(pattern_name='bio_result', permanent=True)),

    url(r'^articles/$', ArticlesView.as_view(), name='bio_articles'),
    url(r'^aricle/(?P<artname>\w+)$', ArticleView.as_view(), name='bio_article')

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
