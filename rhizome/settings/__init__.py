import os
from rhizome.settings.base import *

""" ENV default 'test' """

env = os.environ.get('ENV', 'development')
instance = os.environ.get('INSTANCE', '')

if instance == 'docker':
    from rhizome.settings.docker import *

if env == 'production':
    from rhizome.settings.production import *
elif env == 'test':
    from rhizome.settings.test import *
else:
    from rhizome.settings.development import *
