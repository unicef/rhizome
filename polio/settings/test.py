from polio.settings.base import *

MEDIA_ROOT = 'datapoints/tests/_data/'

SOUTH_TESTS_MIGRATE = False

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
DATABASES['default']['NAME'] = 'rhizome'
