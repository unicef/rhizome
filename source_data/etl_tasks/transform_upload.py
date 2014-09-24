import pprint as pp

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from source_data.models import ProcessStatus, SourceDataPoint, SourceIndicator, IndicatorMap
from datapoints.models import DataPoint, Source


class DocTransform(object):

    def __init__(self,document_id,df,uploaded_by_user_id):

        self.source_datapoints = []

        self.document_id = document_id
        self.df = df
        self.uploaded_by_user_id = uploaded_by_user_id

        self.sheet_df_to_source_datapoints()




    def sheet_df_to_source_datapoints(self):

        cols = [col.lower() for col in self.df]

        for i,(row) in enumerate(self.df.values):

            row_basics = {}
            #
            region_string = row[cols.index('lga')] + '-' + row[cols.index('state')] \
                + '-' + row[cols.index('ward')] + '-' + str(row[cols.index('settlement')])

            row_basics['row_number'] = i
            row_basics['region_string'] = region_string
            row_basics['campaign_string'] = str(row[cols.index('datesoc')])
            row_basics['source_guid'] = row[cols.index('uniquesoc')]
            #
            for i,(cell) in enumerate(row):

                to_create = row_basics
                to_create['indicator_string'] = cols[i]
                to_create['cell_value'] = cell


                to_create['status_id'] = ProcessStatus.objects.get(status_text='TO_PROCESS').id
                to_create['source_id'] = Source.objects.get(source_name='Spreadsheet Upload').id
                to_create['document_id'] = self.document_id

                try:
                    created = SourceDataPoint.objects.create(**to_create)
                    self.source_datapoints.append(created)
                except IntegrityError as e:
                    print e
