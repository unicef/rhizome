from rhizome.settings.base import *

class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES =  DisableMigrations()
MEDIA_ROOT = 'rhizome/tests/_data/'

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
DATABASES['default']['NAME'] = 'rhizome'
