# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import jsonfield.fields
import django.db.models.deletion
from django.db import models, migrations
from django.conf import settings
from django.db.models import get_app, get_models
from django.conf import settings

import pandas as pd

from datapoints.cache_meta import minify_geo_json, LocationTreeCache
from datapoints.models import Location, LocationPolygon
from source_data.models import Document, DocumentDetail, DocDetailType
from source_data.etl_tasks.transform_upload import DocTransform

def populate_source_data(apps, schema_editor):
    '''
    Here, we take an excel file that has the same schema as the database
    we lookup the approriate model and bulk insert.

    We need to ingest the data itself in the same order as the excel
    sheet otherwise we will have foreign key constraint issues.
    '''

    xl = pd.ExcelFile('initial_data.xlsx')
    all_sheets = xl.sheet_names
    source_data_sheets = [s for s in all_sheets if s.startswith('source-data_')]

    for s in source_data_sheets:
        source_sheet_df = xl.parse(s)
        process_source_sheet(source_sheet_df, s)

def process_source_sheet(source_sheet_df, sheet_name):

    user_id = 1 ## sketchy but will work so long as developer creates a
                ## superuser when spinning up a new app

    file_loc = settings.MEDIA_ROOT + sheet_name
    print 'SAVING: ' + file_loc
    source_sheet_df.to_csv(file_loc)

    new_doc = Document.objects.create(
        doc_title = sheet_name,
        created_by_id = user_id,
        guid = 'test',
        docfile=file_loc
    )

    create_doc_details(new_doc.id)

    DocTransform(user_id, new_doc.id)

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
        ('datapoints', '0002_populate_initial_data'),
    ]

    operations = [
        migrations.RunPython(populate_source_data),
    ]
