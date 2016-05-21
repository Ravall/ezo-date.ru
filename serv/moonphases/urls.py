from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from moonphases.views import IndexView, MonthView, MoonPhasesArticles, Article, MoonPhasesMyCity

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='moonphases_home'),
    url(r'^month$', MonthView.as_view(), name='moonphases_month'),
    url(r'^city$', MoonPhasesMyCity.as_view(), name='moonphases_city'),
    url(r'^aricles$', MoonPhasesArticles.as_view(), name='moonphases_articles'),
    url(r'^aricle/(?P<artname>\w+)$', Article.as_view(), name='moonphases_article'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
