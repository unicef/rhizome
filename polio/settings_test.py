from settings import *

SOUTH_TESTS_MIGRATE = True
DATABASES['default'] = {'ENGINE': 'django.db.backends.postgresql_psycopg2',\
    'NAME':'polio'}
