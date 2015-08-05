# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

def forwards_func(apps, schema_editor):
    User.objects.create_user\
        ('john', email='dingeej@gmail.com', password='endpolionow')


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0003_auto_20150805_0809'),
    ]

    operations = [
        migrations.RunPython(
            forwards_func,
        ),
    ]
