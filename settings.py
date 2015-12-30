"""
Django settings for polio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) + '/rhizome'
LOGIN_REDIRECT_URL = '/datapoints'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7i_%j5chyhx2k3#874-!8kwwlcr88sn9blbsb7$%58h&t#n84f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MEDIA_ROOT = '/var/www/apps/rhizome/media/'
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
    'django_cron',
    'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar.panels.sql.SQLPanel',

)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
)

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
	    # 'PASSWORD': 'w3b@p01i0',
        'PASSWORD': '3r@d1c@tep0l!0',
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'apps/rhizome/webapp/public/static')

STATICFILES_DIRS = []


WEBPACK_LOADER = {
    'BUNDLE_DIR_NAME': 'bundles/',
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    'POLL_DELAY': 0.2,
    'IGNORE': ['.+\.hot-update.js', '.+\.map']
}

## API SETTINGS ##

TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 0
TASTYPIE_FULL_DEBUG = True

CRON_CLASSES = [
    "rhizome.cron.AggAndComputeDataPoint",
    "rhizome.cron.MasterRefreshJob",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/logs/django.log',
            },
        },
    'loggers': {
        'django_cron': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


ODK_SETTINGS = {
    'JAR_FILE':'/Users/john/odk/odk_briefcase_v1.4.6_production.jar',
    'RHIZOME_USERNAME':'demo_user',
    'RHIZOME_KEY': '67e16b36d64376ba7bf81233cd63d092d5f8582a',
    'STORAGE_DIRECTORY':'/Users/john/odk/ODK_Briefcase_Storage/',
    'EXPORT_DIRECTORY':'/Users/john/odk/csv_export/',
    'ODK_USER':'mike',
    'ODK_PASS':'nealgoldman',
    'AGGREGATE_URL':'https://map-soweto.appspot.com/',
    'API_ROOT':'http://localhost:8000/api/v1/',
}

