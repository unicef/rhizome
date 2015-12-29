# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction

from datapoints.models import Campaign, Location, DataPointComputed, \
    CampaignToIndicator, DataPoint

def migrate_campaign_data(apps, schema_editor):

    cti_batch = []

    for c in Campaign.objects.all():

        ## update top level location_id ##
        parent_loc_id = Location.objects.get(parent_location_id=None,\
            office_id = c.office_id).id

        c.top_lvl_location_id = parent_loc_id

        ## add display name to campaign ##
        c.name = c.slug
        c.save()

        ## create campaign to indicator relationships ##
        indicator_id_list = DataPointComputed.objects\
            .filter(campaign_id = c.id,location_id = parent_loc_id)\
            .values_list('indicator_id',flat=True)

        for ind_id in indicator_id_list:

            cti_obj = CampaignToIndicator(**{'campaign_id': c.id,
                'indicator_id': ind_id})

            cti_batch.append(cti_obj)

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
        ('datapoints', '0034_datadate_to_datapoint'),
    ]
    operations = [
        migrations.AddField(
            model_name='campaign',
            name='top_lvl_indicator_tag',
            field=models.ForeignKey(default=1, to='datapoints.IndicatorTag'),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_campaign_data)
    ]
