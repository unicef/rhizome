import pprint as pp

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from source_data.models import ProcessStatus, SourceDataPoint, SourceIndicator, IndicatorMap
from datapoints.models import DataPoint, Source

class DocIngest(object):

    def __init__(self,document_id,mappings,df,uploaded_by_user_id):

        self.document_id = document_id
        self.mappings = mappings
        self.df = df
        self.uploaded_by_user_id = uploaded_by_user_id

        self.process_sheet_df()

    def process_sheet_df(self):

        self.sheet_df_to_source_datapoints()
        self.ingest_doc_to_master()

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
                    SourceDataPoint.objects.create(**to_create)
                except IntegrityError as e:
                    print e


    def ingest_doc_to_master(self):

        to_process = SourceDataPoint.objects.filter(document_id=self.document_id)

        for i,(record) in enumerate(to_process):

            self.csv_upload_record_to_datapoint(record)


    def csv_upload_record_to_datapoint(self,record):

        try:
            indicator_id = self.mappings['indicators'][record.indicator_string]
            print 'INDICATOR ID: ' + str(indicator_id)
        except KeyError:
            return

        try:
            region_id = self.mappings['regions'][record.region_string]
            print 'REGION ID: ' + str(region_id)
        except KeyError:
            return

        try:
            campaign_id = self.mappings['campaigns'][record.campaign_string]
            print 'CAMPAIGN ID: ' + str(campaign_id)
        except KeyError:
            print 'THIS CAMPAIGN DIDNT WORK: ' + record.campaign_string
            print self.mappings['campaigns']
            return

        try:
            datapoint, created = DataPoint.objects.get_or_create(
                indicator_id = indicator_id,
                region_id = region_id,
                campaign_id = campaign_id,
                value = record.cell_value,
                source_id = Source.objects.get(source_name='Spreadsheet Upload').id,
                changed_by_id = self.uploaded_by_user_id,
                source_guid = record.guid
            )

        except Exception as e:
            print e
