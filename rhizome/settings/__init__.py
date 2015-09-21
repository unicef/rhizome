import os
from rhizome.settings.base import *

""" ENV default 'development' """

env = os.environ.get('ENV', 'development')
instance = os.environ.get('INSTANCE', '')

if instance == 'docker':
    from polio.settings.docker import *

if env == 'production':
    from polio.settings.production import *
elif env == 'test':
    from polio.settings.test import *
else:
    from rhizome.settings.development import *
