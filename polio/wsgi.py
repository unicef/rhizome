"""
WSGI config for polio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/var/www/clients.seedscientific.com/uf/polio')
sys.path.append('/var/www/clients.seedscientific.com/uf/polio/polio')

os.environ['DJANGO_SETTINGS_MODULE'] = 'prod_settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()