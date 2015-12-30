import os
from rhizome.settings.base import *

""" ENV default 'test' """

env = os.environ.get('ENV', 'test')
instance = os.environ.get('INSTANCE', '')

if instance == '':
    from rhizome.settings.base import *

if instance == 'docker':
    from rhizome.settings.docker import *

if env == 'production':
    from rhizome.settings.production import *
elif env == 'test':
    from rhizome.settings.test import *

## import ODK_SETTING, and anything specifc to personal development ##
## for instance if you need an API key from rapid pro, you would store it
## in development settings ##

try:
    from rhizome.settings.private import *
except ImportError:
    pass
