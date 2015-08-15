# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('source_data', '0009_sourcesubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceObjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('master_object_id', models.IntegerField()),
                ('source_object_code', models.CharField(max_length=255)),
                ('content_type', models.CharField(max_length=10)),
                ('mapped_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'source_object_map',
            },
        ),
        migrations.AlterUniqueTogether(
            name='sourceobjectmap',
            unique_together=set([('content_type', 'source_object_code')]),
        ),
        migrations.RunSQL('''
        -- INSERT INTO source_object_map
        -- (content_type, source_object_code, mapped_by_id, master_object_id)

        SELECT
        	'region'
        	,sr.region_code
        	,rm.mapped_by_id
        	,rm.master_object_id

        FROM source_region sr
        INNER JOIN region_map rm
        ON sr.id = rm.source_object_id

        UNION ALL

        SELECT
        	'campaign'
        	,sc.campaign_string
        	,cm.mapped_by_id
        	,cm.master_object_id
        FROM source_campaign sc
        INNER JOIN campaign_map cm
        ON sc.id = cm.source_object_id


        UNION ALL

        SELECT
        	'indicator'
        	,si.indicator_string
        	,im.mapped_by_id
        	,im.master_object_id
        FROM source_indicator si
        INNER JOIN indicator_map im
        ON si.id = im.source_object_id;




        ''')

    ]
