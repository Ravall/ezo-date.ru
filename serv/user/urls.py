from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user.views import AjaxCity


urlpatterns = patterns('',
#    url(r'^registration$', RegView.as_view(), name='user_registration'),
#    url(r'^avatar/', include('avatar.urls')),
    url(r'^ajax/city$', AjaxCity.as_view(), name='ajax_city_autocomplete'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
