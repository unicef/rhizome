# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0005_cache_and_cleanup_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionTree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lvl', models.IntegerField()),
                ('immediate_parent', models.ForeignKey(related_name='immediate_parent', to='datapoints.Region')),
                ('parent_region', models.ForeignKey(related_name='ultimate_parent', to='datapoints.Region')),
                ('region', models.ForeignKey(to='datapoints.Region')),
            ],
            options={
                'db_table': 'region_tree',
            },
        ),
        migrations.AlterUniqueTogether(
            name='docdatapoint',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='regiontree',
            unique_together=set([('parent_region', 'region')]),
        ),
    ]
