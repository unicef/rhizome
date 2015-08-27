# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('source_data', '0004_auto_20150827_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocDetailType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'document_detail_type',
            },
        ),
        migrations.RunSQL('''

            INSERT INTO document_detail_type
            (name)
            SELECT 'odk_host' UNION ALL
            SELECT 'odk_form_name' UNION ALL
            SELECT 'region_column' UNION ALL
            SELECT 'campaign_column' UNION ALL
            SELECT 'username_column' UNION ALL
            SELECT 'uq_id_column' UNION ALL
            SELECT 'agg_on_region' UNION ALL
            SELECT 'image_col' UNION ALL
            SELECT 'delimiter' UNION ALL
            SELECT 'submission_count' UNION ALL
            SELECT 'submission_processed_count' UNION ALL
            SELECT 'doc_datapoint_count' UNION ALL
            SELECT 'datapoint_count' UNION ALL
            SELECT 'agg_datapoint_count' UNION ALL
            SELECT 'calc_datapoint_count' UNION ALL
            SELECT 'lat_col' UNION ALL
            SELECT 'lon_col';

            TRUNCATE TABLE document_detail;
        '''
        ),

        migrations.RemoveField(
            model_name='documentdetail',
            name='doc_detail_type',
        ),

        migrations.AddField(
                model_name='documentdetail',
                name='doc_detail_type',
                field=models.ForeignKey(blank=True, to='source_data.DocDetailType'),
                preserve_default=False,
            ),

        # migrations.AlterField(
        #     model_name='documentdetail',
        #     name='doc_detail_type',
        #     field=models.ForeignKey(to='source_data.DocDetailType'),
        # ),
    ]
