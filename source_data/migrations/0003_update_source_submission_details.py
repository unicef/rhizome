# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0020_chart_type_schema'),
        ('source_data', '0002_migrate_submission_campaign_and_location'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            UPDATE source_submission ss
            SET campaign_code = sd.campaign_code,
                location_code = sd.location_code,
                campaign_id = sd.campaign_id,
                location_id = sd.location_id
            FROM submission_detail sd
            WHERE ss.document_id = sd.document_id
            AND ss.id = sd.source_submission_id;
            '''
        ),
    ]
