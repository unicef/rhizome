# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import jsonfield.fields

from rhizome.etl_tasks.transform_upload import DateDocTransform
from rhizome.models import *
import pandas as pd

def ingest_polio_cases(apps, schema_editor):


    indicator_id = Indicator.objects.create(
        name = 'Polio Cases',
        short_name = 'Polio Cases',
        description = 'Polio Cases',
    )

    process_source_sheet_df()

    polio_cases_count = DataPoint.objects.filter(
        indicator_id = indicator_id,
    ).count()

    print 'polio case count\n' * 10

    if polio_cases_count != target_case_count:
        raise Exception('did not ingest the polio case data properly')


def process_source_sheet_df():

    user_id = 1
    sheet_name = 'AfgPolioCases.csv'
    # file_loc = settings.MEDIA_ROOT + sheet_name
    # saved_csv_file_location = settings.MEDIA_ROOT + sheet_name

    source_sheet_df = pd.read_csv(sheet_name)

    print '===\n' * 3
    print source_sheet_df[:2]
    print '===\n' * 3

    # doc_file_text = sheet_name + '.csv'

    new_doc = Document.objects.create(
        doc_title = sheet_name,
        guid = 'test'
    )

    # create_doc_details(new_doc.id)

    ## document -> source_submissions ##
    dt = DateDocTransform(user_id, new_doc.id, source_sheet_df)
    dt.process_file()

    ## source_submissions -> datapoints ##
    mr = MasterRefresh(user_id, new_doc.id)
    mr.main()

    ## datapoints -> computed datapoints ##
    # for c in Campaign.objects.all():
    #     print 'processing campaign id: %s' % c.id
    #     ar = AggRefresh(c.id)
    #     print 'DWC COUNT %s' % len(DataPointComputed.objects\
    #         .filter(campaign_id = c.id))

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0011_customdashboard_rows'),
    ]

    operations = [
        migrations.RunPython(ingest_polio_cases)
    ]
