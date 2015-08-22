from settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {'ENGINE': 'django.db.backends.postgresql_psycopg2',\
    'NAME':'polio'}
