# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0011_customdashboard_rows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='campaign',
            field=models.ForeignKey(to='rhizome.Campaign', null=True),
        ),
        migrations.AlterField(
            model_name='docdatapoint',
            name='campaign',
            field=models.ForeignKey(to='rhizome.Campaign', null=True),
        ),
    ]

# insert into datapoint
# ( data_date, value, created_at, cache_job_id, indicator_id, location_id, source_submission_id)
