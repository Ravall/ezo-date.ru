# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from user.views import ActivationView, RegistrationView, ProfileView, PasswordChangeView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/', None)

urlpatterns = patterns(
    '',
    url(
        r'^register/$',
        login_forbidden(RegistrationView.as_view()),
        name='registration_register'
    ),
    url(
        r'^login/$',
        login_forbidden(auth_views.login), {
        'template_name': 'registration/login.html',
        'extra_context': {'service': 'login'}},
        name='auth_login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='auth_logout'
    ),
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'
    ),
    url(
        r'^activate/complete/$',
        login_forbidden(TemplateView.as_view(
            template_name='registration/activation_complete.html',
            get_context_data=lambda:{'service': 'registration'},
        )),
        name='registration_activation_complete',

    ),
    url(
        r'^register/complete/$',
        login_forbidden(TemplateView.as_view(
            template_name='registration/registration_complete.html',
            get_context_data=lambda:{'service': 'registration'},
        )),
        name='registration_complete'
    ),
    url(
        r'^register/closed/$',
        login_forbidden(TemplateView.as_view(
           template_name='registration/registration_closed.html',
           get_context_data=lambda:{'service': 'registration'},
        )),
        name='registration_disallowed'
    ),


    url(r'^access/$', login_required(PasswordChangeView.as_view()), name='auth_settings'),

    url(
        r'^password/reset/$',
        login_forbidden(auth_views.password_reset),
        {'post_reset_redirect': 'auth_password_reset_done',
         'email_template_name': 'registration/password_reset_email.txt',
         'extra_context': {'service': 'login'}},
        name='auth_password_reset'
    ),
    url(
        r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        login_forbidden(auth_views.password_reset_confirm),
        {
           'post_reset_redirect': 'auth_password_reset_complete',
            'extra_context': {'service': 'login'}
        },
        name='auth_password_reset_confirm'
    ),
    url(
        r'^password/reset/complete/$',
        login_forbidden(auth_views.password_reset_complete),
        {'extra_context': {'service': 'login'}},
        name='auth_password_reset_complete'),

    url(
        r'^password/reset/done/',
        login_forbidden(auth_views.password_reset_done),
        {'extra_context': {'service': 'login'}},
        name='auth_password_reset_done'
    ),
    url(r'', include('registration.backends.model_activation.urls')),
    url(r'', include('user.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
