# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
from django.core.exceptions import ImproperlyConfigured

from django.core.management import call_command
from django.conf import settings
from django.db import connection
from django.db.models.loading import get_app
from StringIO import StringIO
from datetime import datetime

from rhizome.models import CacheJob


def reset_seq(apps, schema_editor):
    '''
    This has to do with Autoincrement... Since we insert PKs directly in
    "populate inital metadata", the DB engine still thinks that it needs
    to assign "1" to the first indicator fr instance that is created.

    By resetting the sequence, we ensure that the ORM will add add sequential
    IDs relative to what we created in the inital migrations
    '''

    cj_1 = CacheJob.objects.create(
        id=1,
        date_attempted=datetime.now(),
        date_completed=datetime.now(),
        is_error=False
    )

    os.environ['DJANGO_COLORS'] = 'nocolor'

    commands = StringIO()
    cursor = connection.cursor()

    for app in ['rhizome', 'django.contrib.auth']:
        try:
            label = app.split('.')[-1]
            if get_app(label):
                call_command('sqlsequencereset', label, stdout=commands)
        except Exception as err:
            pass
    try:
        cursor.execute(commands.getvalue())
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0004_populate_fake_computed_data'),
    ]

    operations = [
        migrations.RunPython(reset_seq),
    ]
