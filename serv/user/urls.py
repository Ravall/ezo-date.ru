from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user.views import ProfileView
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView


urlpatterns = patterns(
    '',
    url(r'^profile/$', login_required(ProfileView.as_view()), name='user_profile'),
    url(r'^$', RedirectView.as_view(url='/user/profile', permanent=False)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
