
## test settings and globals that allow
## us to run our tests suite locally

PROJECT_ROOT = '/Users/johndingee_seed/code/polio/' ## FIXX!!
# from .base import *  ## this isnt working (it should give me project root)

SECRET_KEY = '7i_%j5chyhx2k3#874-!8kwwlcr88sn9blbsb7$%58h&t#n84f'


###### TEST SETTINGS


TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT
TEST_DISCOVER_ROOT = PROJECT_ROOT
TEST_DISCOVER_PATTERN = "test_*"

####### IN MEMORY TEST DATABASE #######
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "memory",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": ""
    }
}