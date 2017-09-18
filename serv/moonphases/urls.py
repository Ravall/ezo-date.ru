from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from moonphases import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='moonphases_home'),
    url(r'^month/$', views.MonthView.as_view(), name='moonphases_month'),
    url(r'^aricles/$', views.MoonPhasesArticles.as_view(), name='moonphases_articles'),
    url(r'^aricle/(?P<artname>\w+)/$', views.Article.as_view(), name='moonphases_article'),

    url(r'^form/$', views.MoonPhasesForm.as_view(), name='moonphases_form'),
    url(r'^result/$', views.MoonPhasesFormResult.as_view(), name='moonphases_form_result'),

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
