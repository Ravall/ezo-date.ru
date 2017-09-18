from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from suntime import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='suntime_home'),
    url(r'^articles/$', views.ArticlesView.as_view(), name='suntime_articles'),
    url(r'^aricle/(?P<artname>\w+)/$', views.ArticleView.as_view(), name='suntime_article'),
    url(r'^form/$', views.ArticlesFormView.as_view(), name='suntime_form'),
    url(r'^result/$', views.ArticlesFormResultView.as_view(), name='suntime_form_result'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
