# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
from StringIO import StringIO

from django.core.management import call_command
from django.db import connection
from django.db.models.loading import get_app

def reset_seq(apps, schema_editor):

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
