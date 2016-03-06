# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models

import pandas as pd

from rhizome.cache_meta import minify_geo_json, LocationTreeCache
from rhizome.models import Location, LocationPolygon
from rhizome.models import Document, DocumentDetail, DocDetailType
from rhizome.etl_tasks.transform_upload import DocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.agg_tasks import AggRefresh

def populate_source_data(apps, schema_editor):
    '''
    Here, we take an excel file that has the same schema as the database
    we lookup the approriate model and bulk insert.

    We need to ingest the data itself in the same order as the excel
    sheet otherwise we will have foreign key constraint issues.
    '''
    pass

    # xl = pd.ExcelFile('initial_data.xlsx')
    # all_sheets = xl.sheet_names
    # source_data_sheets = [s for s in all_sheets if s.startswith('source-data_')]
    #
    # for s in source_data_sheets:
    #     source_sheet_df = xl.parse(s)
    #     process_source_sheet(source_sheet_df, s)

def process_source_sheet(source_sheet_df, sheet_name):

    user_id = -1

    # file_loc = settings.MEDIA_ROOT + sheet_name
    saved_csv_file_location = settings.MEDIA_ROOT + sheet_name + '.csv'
    source_sheet_df.to_csv(saved_csv_file_location)
    doc_file_text = sheet_name + '.csv'

    new_doc = Document.objects.create(
        doc_title = doc_file_text,
        guid = 'test',
        docfile=doc_file_text
    )

    create_doc_details(new_doc.id)

    ## document -> source_submissions ##
    dt = DocTransform(user_id, new_doc.id)
    dt.main()

    ## source_submissions -> datapoints ##
    mr = MasterRefresh(user_id, new_doc.id)
    mr.main()

    ## datapoints -> computed datapoints ##
    ar = AggRefresh()

def create_doc_details(doc_id):

    doc_detail_types = ['uq_id_column', 'date_column', 'location_column']

    for dd_type in doc_detail_types:
        DocumentDetail.objects.create(
            document_id = doc_id,
            doc_detail_type_id = DocDetailType.objects.get(name = dd_type).id,
            doc_detail_value = dd_type ## this implies that the source columns
                                        ## are named with the above convention
        )

class Migration(migrations.Migration):

    dependencies = [
        ('rhizome', '0002_populate_initial_meta_data'),
    ]

    operations = [
        migrations.RunPython(populate_source_data),
    ]
