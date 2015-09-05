# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from os import path

SQL_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'sql')


def readSQLFromFile(filename):
    return open(path.join(SQL_DIR, filename), 'r').read()


class Migration(migrations.Migration):
    dependencies = [
        ('source_data', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(readSQLFromFile('functions/fn_upsert_source_dps.sql'))
    ]
