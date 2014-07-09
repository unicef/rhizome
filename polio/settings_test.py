from settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# from project root run:
    # python manage.py test --settings=polio.settings_test
    # coverage run manage.py test --settings=polio.settings_test


    # python manage.py test datapoints --settings=polio.settings_test
    # coverage run manage.py test datapoints --settings=polio.settings_test

    