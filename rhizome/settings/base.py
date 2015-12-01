"""
Django settings for polio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = '/static/'

# todo for hashed we can use this http://blogs.skicelab.com/maurizio/django-serving-hashed-static-files-with-nginx.html

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'webapp/public/static')
]

LOGIN_REDIRECT_URL = '/datapoints'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7i_%j5chyhx2k3#874-!8kwwlcr88sn9blbsb7$%58h&t#n84f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'source_data',
    'datapoints',
    'coverage',
    'simple_history',
    'tastypie',
    'debug_toolbar',
    'django_cron',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.sql.SQLPanel',

)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
)

CRON_CLASSES = [
    "rhizome.cron.AggAndComputeDataPoint",
    "rhizome.cron.MasterRefreshJob",
    "rhizome.cron.MetaRefreshJob",
]

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'rhizome.urls'
WSGI_APPLICATION = 'rhizome.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rhizome',
        'USER': 'djangoapp',
        'PASSWORD': 'w3b@p01i0',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Template configuration
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

## API SETTINGS ##

TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 0
TASTYPIE_FULL_DEBUG = True

INTERNAL_IPS=('127.0.0.1',)
