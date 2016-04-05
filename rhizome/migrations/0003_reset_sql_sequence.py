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

    cj_1 = CacheJob.objects.create(
        id = 1,
        date_attempted = datetime.now(),
        date_completed = datetime.now(),
        is_error = False
    )

    os.environ['DJANGO_COLORS'] = 'nocolor'

    commands = StringIO()
    cursor = connection.cursor()

    for app in ['rhizome', 'django.contrib.auth']:
        label = app.split('.')[-1]
        if get_app(label):
                call_command('sqlsequencereset', label, stdout=commands)
        cursor.execute(commands.getvalue())

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0002_populate_initial_meta_data'),
    ]

    operations = [
        migrations.RunPython(reset_seq),
    ]
