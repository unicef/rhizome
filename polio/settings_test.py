from settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# from project root run:

    # coverage run manage.py test datapoints --settings=polio.settings_test 
    # coverage html --omit='venv/*.py,datapoints/tests/*.py'

    