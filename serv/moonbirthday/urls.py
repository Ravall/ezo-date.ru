from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from moonbirthday.views import index, all_nums, birthday_num
from moonbirthday.views.ajax import autocomplete_city, get_countries, get_regions, get_city

urlpatterns = patterns('',
    url(r'^$', index.MoonbirthdayIndex.as_view(), name='moon_birthday_home'),
    url(r'^(?P<digit>[0-9]+)_lunnyy_den_rozhdeniya/$', birthday_num.MoonbirthdayNum.as_view(), name='moon_birthday_num'),
    url(r'^all/$', all_nums.MoonbirthdayAllNums.as_view(), name='moon_birthday_all_nums'),
    url(r'^ajax/city$', autocomplete_city.Ajax.as_view(), name='ajax_city_autocomplete'),
    url(r'^ajax/get_countries$', get_countries.Ajax.as_view(), name='ajax_get_countries'),
    url(r'^ajax/get_regions$', get_regions.Ajax.as_view(), name='ajax_get_regions'),
    url(r'^ajax/get_city$', get_city.Ajax.as_view(), name='ajax_get_city'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
