# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction

from datapoints.models import Campaign, Location, DataPointComputed, \
    CampaignToIndicator, DataPoint, IndicatorTag

from source_data.models import DocDetailType


def change_campaign_column_to_date_column(apps, schema_editor):

    dtt = DocDetailType.objects.get(name='campaign_column')
    dtt.name = 'date_column'
    dtt.save()

def migrate_campaign_data(apps, schema_editor):

    cti_batch = []

    for c in Campaign.objects.all():

        ## update top level location_id ##
        parent_loc_id = Location.objects.get(parent_location_id=None,\
            office_id = c.office_id).id
        c.top_lvl_location_id = parent_loc_id

        ## create campaign to indicator relationships ##
        parent_tag_id = IndicatorTag.objects.get(tag_name='Polio').id
        c.top_lvl_indicator_tag_id = parent_tag_id

        ## add display name to campaign ##
        c.name = c.slug
        c.save()

        ## add appropriate data date to campaign table ##
        datapoint_qs = DataPoint.objects.raw('''
            UPDATE datapoint d
            SET d.data_date = c.start_date
            FROM campaign c
            WHERE d.campaign_id = c.id
            AND c.id = %s;

            SELECT id from datapoint limit 1;
        ''',[c.id])


    CampaignToIndicator.objects.all().delete()
    CampaignToIndicator.objects.bulk_create(cti_batch)


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0035_campaign_top_lvl_indicator_tag'),
    ]
    operations = [
        migrations.RunPython(migrate_campaign_data),
        migrations.RunPython(change_campaign_column_to_date_column)
    ]
