from settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# from project root run:
    # python manage.py test --settings=polio.test_settings
    # coverage run manage.py test --settings=polio.test_settings