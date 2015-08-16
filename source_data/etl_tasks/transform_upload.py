from pandas import read_csv
from pandas import notnull
from pprint import pprint

from django.conf import settings
from django.db import transaction
from pandas.io.excel import read_excel

from source_data.models import *
from source_data.etl_tasks.shared_utils import pivot_and_insert_src_datapoints
from datapoints.models import DataPoint


class DocTransform(object):

    def __init__(self,document_id):

        self.source_datapoints = []
        self.document_id = document_id

        self.file_path = str(Document.objects.get(id=self.document_id).docfile)
        self.to_process_status = ProcessStatus.objects.get(status_text='TO_PROCESS').id


    def prep_file(self,full_file_path):

        f_header = open(full_file_path,'r')
        self.file_header = f_header.readlines()[0]
        f_header.close()

        f = open(full_file_path,'r')
        file_stream = f.readlines()[1:]

        return file_stream

    def dp_df_to_source_datapoints(self):

        full_file_path = settings.MEDIA_ROOT + self.file_path
        file_stream = self.prep_file(full_file_path)
        file_row_count = len(file_stream)

        batch = []
        for i,(submission) in enumerate(file_stream):
            submission_dict = {
                'submission_json': dict(zip(self.file_header, submission)),
                'document_id': self.document_id,
                'row_number': i,
                'instance_guid': i,
            }
            batch.append(SourceSubmission(**submission_dict))

        SourceSubmission.objects.bulk_create(batch)


class RegionTransform(DocTransform):


    def validate(self):

        essential_columns = ['name','code','parent_name','region_type','country','lat','lon','high_risk_2014','parent_code']
        df_cols = [col for col in self.df]
        intsct = list(set(essential_columns).intersection(df_cols))

        if sorted(essential_columns) == sorted(intsct):
            valid_df = self.df[essential_columns]

            return None,valid_df

        else:
            err = 'must have all of the following columns: ' + str(essential_columns)
            return err,None


    def insert_source_regions(self,valid_df):
        ''' in this method we take a datframe go through and create a source region
        for each record.  If the source region exists ( the string exists ), we
        update that record with the new values.  After this, we do the same with
        the parent regions.  One fall back currently is that the only conflict
        resolution for this is the fact that newer records take precedence.  This
        means for instance that if you upload a region with no lon/lat it could
        override the same region that currently has lon/lat'''

        valid_df['region_name'] = valid_df['name'] # unable to access name attr directly... fix this

        just_created, updated, errors = [],[],[]

        for row in valid_df.iterrows():

            row_data = row[1]

            sr = SourceRegion.objects.get_or_create(
                region_string = row_data.region_name,\
                region_type  = row_data.region_type,\
                country = row_data.country,
                region_code = row_data.code,\
                parent_name = row_data.parent_name,\
                lat = row_data.lat,\
                lon = row_data.lon,\
                document_id = self.document_id,\
                parent_code = row_data.parent_code,
                source_guid = str(self.document_id) + '-' + str(row_data.code))

            just_created.append(sr)
