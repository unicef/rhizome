"""
Django settings for polio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

STATIC_URL = '/static/'
SITE_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '')
STATIC_ROOT = os.path.join(SITE_ROOT, '../static')

# todo for hashed we can use this
# http://blogs.skicelab.com/maurizio/django-serving-hashed-static-files-with-nginx.html

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'webapp/public/static')
]

LOGIN_REDIRECT_URL = '/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', '7i_%j5chyhx2k3#874-!8kwwlcr88sn9blbsb7$%58h&t#n84f')

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
    'coverage',
    'simple_history',
    'rhizome',
    'tastypie',
    'corsheaders',
    'debug_toolbar',
    'waffle'
)

CORS_ORIGIN_ALLOW_ALL = True # should be upated to only allow our websites

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'waffle.middleware.WaffleMiddleware'
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

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'rhizome.urls'
WSGI_APPLICATION = 'rhizome.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'rhizome'),
        'USER': os.getenv('DB_USER', 'djangoapp'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'w3b@p01i0'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}

ODK_SETTINGS = {
    # download here:
    # https://opendatakit.org/downloads/download-info/odk-briefcase/
    'JAR_FILE': '',
    'RHIZOME_USERNAME': '',
    # 'get an API key.. http://stackoverflow.com/questions/10940983/
    'RHIZOME_KEY': '',
    'STORAGE_DIRECTORY': '',  # /my/storage/dir',
    'EXPORT_DIRECTORY': '',  # ' /my/output/dir,
    'ODK_USER': '',  # my_odk_username
    'ODK_PASS': '',  # my_odk_password
    'AGGREGATE_URL': '',  # :'https://my-odk-server.appspot.com/',
    'API_ROOT': 'http://localhost:8000/api/v1/',
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Template configuration
# TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'templates'),
#)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Our template directory
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

## API SETTINGS ##

TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 0
TASTYPIE_FULL_DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)


## Customization SETTINGS ##
ABOUT_HTML = "<p> Rhizomes are underground systems that produce stems and roots of plants, allowing them to grow and thrive. They store nutrients that help plants survive and regenerate in the most challenging conditions. Ceaselessly establishing new connections between them, rhizomes constitute resilient, flexible and dynamic systems, rooted in their local environments and primed for long-term sustainability. <p> Rhizome DB supports the polio programme's ritical need to adapt, evolve and reach the unreached. Rhizome DB connects staff, managers and policy makers to the evidence they need to drive local solutions. Maximize your impact to eradicate polio.</p>"
# write the name of the logo with its extention (it should be without space)
# The file must be placed the webapp/src/assests/img folder
LOGO_FILENAME = os.getenv('LOGO_FILENAME', 'layout_set_logo.png')
# Logo ALT name
LOGO_ALT = os.getenv('LOGO_ALT', 'Rhizome')

# Flags for the Menu (SOP, C4D, Data)
FLAG_SOP = True
FLAG_C4D = False
FLAG_DATA = True
