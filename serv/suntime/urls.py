from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from suntime.views import IndexView, ChangeCity, ArticlesView, ArticleView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='suntime_home'),
    url(r'^city/$', ChangeCity.as_view(), name='suntime_city'),
    url(r'^articles/$', ArticlesView.as_view(), name='suntime_articles'),
    url(r'^aricle/(?P<artname>\w+)$', ArticleView.as_view(), name='suntime_article'),
    
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
