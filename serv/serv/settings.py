# -*- coding: utf-8 -*-
import sys
import platform
import os
import raven

SECRET_KEY = '#xrq3fac1=ehd2sh0$18&oy(da7@ae=d+8hox3v+t$4*g6d)u9'
DEBUG = platform.node().lower() != 'sancta'
TEMPLATE_DEBUG = DEBUG


# ---- DIRS ----
# PATH - путь к manage.py
PATH = os.path.abspath(os.path.dirname(__file__) + '/../')
DIRECTORY = os.path.abspath(
    os.path.join(PATH, '../', 'files', 'upload')
)
MEDIA_ROOT = os.path.abspath(os.path.join(PATH, '../', 'files', 'media'))
STATIC_ROOT = os.path.abspath(
    os.path.join(PATH, '../', 'files', 'collected_static')
)
STATICFILES_DIRS = (MEDIA_ROOT,)
TEMPLATE_DIRS = (os.path.join(PATH, '../', 'templates'),)
GEOIP_PATH = os.path.abspath(os.path.join(PATH, '../', 'files', 'GEO'))

COMPASS_INPUT = os.path.abspath(os.path.join(MEDIA_ROOT, 'scss'))
COMPASS_OUTPUT = os.path.abspath(os.path.join(MEDIA_ROOT, 'css'))

if DEBUG:
    path = os.path.realpath('../snct_date')
    sys.path.append(path)
else:
    sys.path.append('/home/www/snct_date')




# ---- /DIRS ----


# ---- URLS ----
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
FAVICONPATH = STATIC_URL + 'img/favicon.ico'
FAVICON_PATH = STATIC_URL + 'img/favicon.ico'
# ---- /URLS ----





TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = False
SITE_ID = 1


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django_mobile.context_processors.flavour',
    'serv.context_processors.debug',
    'serv.context_processors.site_name',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    #'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'






INSTALLED_APPS = (

    # веб сервер
    'gunicorn',
    # все то, что предоставляется
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.redirects',
    'registration',
    # scss
    'djcompass',
    #robot
    'robots_txt',
    #favion
    'favicon',
    ###
#    'avatar',
    ###
    'user',
    'serv',
    'biorythms',
    'numerology',
    'moonbirthday',
    'solar',
    'moonphases',
    'suntime',
    'raven.contrib.django.raven_compat',
    'pytils',
    'django.contrib.humanize',
    'django_geoip',
    'snct_date',
    'django_mobile',
    
    'frontend',
    'services',
    'debug_toolbar',

)

#TEST_NON_SERIALIZED_APPS = (
#    'avatar',
#)

#REGISTRATION_AUTO_LOGIN = False
#REGISTRATION_FORM = 'user.forms.form.RegForm'
#INCLUDE_REGISTER_URL = False
#SEND_ACTIVATION_EMAIL = True
#REGISTRATION_OPEN = True
#DEFAULT_FROM_EMAIL = 'admin@ezo-date.ru'
LOGIN_REDIRECT_URL = '/user/profile/'
LOGIN_URL = '/user/login/'

ACCOUNT_ACTIVATION_DAYS = 2
REGISTRATION_OPEN = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}




COMPASS_STYLE = 'compressed'



if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sancta_serv',
            'USER': 'sancta_serv_user',
            'PASSWORD': 'gBEluZ0LDRun',
            'HOST': '127.0.0.1',
            'PORT': '',
            'TEST': {
                'NAME': 'sancta_serv_test',
            },


        }
    }

else:
    from production import DATABASES


API_URL = 'http://api.sancta.ru'

ALLOWED_HOSTS = ['ezo-date.ru', '127.0.0.1']


ROOT_URLCONF = 'serv.urls'
WSGI_APPLICATION = 'serv.wsgi.application'


CACHE_API_TIMEOUT = 60*60*24*3
CACHE_API_TIMEOUT_FAST = 60*1


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/cache'
    },
}

GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'
GEO_CITY_DAT_FILE = GEOIP_PATH + '/' + GEOIP_CITY




if not DEBUG:
    RAVEN_CONFIG = {
        'dsn': 'https://6da2125ce6b84aef8e3af4f28dbda5dc:5899748be08044529283495cdcffa09a@sentry.io/224338',
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    }

MOONBIRTHDAY = {
    'default_city': 'Москва',
    'default_city_id': 524901,
}


IPGEOBASE_ALLOWED_COUNTRIES = ['RU', 'UA']

INTERNAL_IPS = ['127.0.0.1']


LOCALE_PATHS = (
    os.path.join(PATH, '../', 'locale'),
)

APPEND_SLASH = True

