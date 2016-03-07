import json

from pandas import read_csv
from pandas import notnull
from django.conf import settings

from rhizome.models import *
from rhizome.etl_tasks.transform_upload import DocTransform

class SimpleDocTransform(DocTransform):
    '''
    Based on a very specific pre/intra/post campaign template, we sync data
    and don't ask questions.
    '''

    def __init__(self,user_id,document_id):

        self.location_column, self.campaign_column, self.uq_id_column = \
            ['geocode', 'campaign', 'unique_key']

        self.document = Document.objects.get(id=document_id)
        self.file_path = str(self.document.docfile)

        raw_csv_df = read_csv(settings.MEDIA_ROOT + self.file_path)
        csv_df = raw_csv_df.where((notnull(raw_csv_df)), None)
        csv_df[self.uq_id_column] = csv_df[self.location_column].map(str)+ csv_df[self.campaign_column]

        self.csv_df = csv_df

        self.file_header = csv_df.columns

        self.meta_lookup = {
            'location':{},
            'indicator':{},
            'campaign':{}
        }

        self.build_meta_lookup()

        return super(SimpleDocTransform, self).__init__(user_id,document_id)

    def build_meta_lookup(self):
        ## build location lookup ##
        location_lookup = SourceObjectMap.objects\
            .filter(content_type='location',\
                source_object_code__in=list(self.csv_df[self.location_column]))\
            .values_list('source_object_code','master_object_id')

        for source_object_code, master_object_id in location_lookup:
            self.meta_lookup['location'][source_object_code] = master_object_id

        ## build campaign lookup ##
        campaign_lookup = SourceObjectMap.objects\
            .filter(content_type='campaign',\
                source_object_code__in=list(self.csv_df[self.campaign_column]))\
            .values_list('source_object_code','master_object_id')

        for source_object_code, campaign_id in campaign_lookup:
            self.meta_lookup['campaign'][source_object_code] = campaign_id

        ## build indicator lookup ##
        indicator_lookup = SourceObjectMap.objects\
            .filter(content_type='indicator',\
                source_object_code__in=self.file_header)\
            .values_list('source_object_code','master_object_id')

        for source_object_code, indicator_id in indicator_lookup:
            self.meta_lookup['indicator'][source_object_code] = indicator_id


    def main(self):

        self.file_to_source_submissions()

        for row in SourceSubmission.objects.filter(document_id = \
            self.document.id):

            self.process_source_submission(row)

    def process_raw_source_submission(self, submission):

        submission_ix, submission_data = submission[0], submission[1:]

        submission_data = dict(zip(self.file_header,submission_data))
        instance_guid = submission_data[self.uq_id_column]

        if instance_guid == '' or instance_guid in self.existing_submission_keys:
            return None, None

        submission_dict = {
            'submission_json': submission_data,
            'document_id': self.document.id,
            'row_number': submission_ix,
            'location_code': submission_data[self.location_column],
            'campaign_code': submission_data[self.campaign_column],
            'instance_guid': submission_data[self.uq_id_column],
            'process_status': 'TO_PROCESS',
        }

        return submission_dict, instance_guid


    def process_source_submission(self,row):

        dwc_batch, dwc_list_of_lists = [], []
        submission  = row.submission_json


        location_id = self.meta_lookup['location'][row.location_code]
        campaign_id = self.meta_lookup['campaign'][row.campaign_code]

        for k,v in submission.iteritems():

            try:
                indicator_id = self.meta_lookup['indicator'][k]
            except KeyError:
                indicator_id = None

            if indicator_id:

                dwc_obj = DataPointComputed(**{
                        'location_id': location_id,
                        'indicator_id' : indicator_id,
                        'campaign_id': campaign_id,
                        'value': v,
                        'cache_job_id': -1,
                        'document_id': self.document.id
                    })
                dwc_batch.append(dwc_obj)
                dwc_list_of_lists.append([location_id,indicator_id,campaign_id])

        dwc_ids_to_delete = self.get_dwc_ids_to_delete(dwc_list_of_lists)
        DataPointComputed.objects.filter(id__in=dwc_ids_to_delete).delete()
        DataPointComputed.objects.bulk_create(dwc_batch)

    def get_dwc_ids_to_delete(self, dwc_list_of_lists):

        df = DataFrame(dwc_list_of_lists, columns=['location_id', \
            'indicator_id', 'campaign_id'])

        uq_location_id_list = list(df['location_id'].unique())
        uq_indicator_id_list = list(df['indicator_id'].unique())
        uq_campaign_id_list = list(df['campaign_id'].unique())

        dwc_location_ids = DataPointComputed.objects.filter(location_id__in=
            uq_location_id_list).values_list('id',flat=True)

        dwc_indicator_ids = DataPointComputed.objects.filter(indicator_id__in=
            uq_indicator_id_list).values_list('id',flat=True)

        dwc_campaign_ids = DataPointComputed.objects.filter(campaign_id__in=
            uq_campaign_id_list).values_list('id',flat=True)

        ids_to_delete = set.intersection(*map(set,\
            [dwc_location_ids,dwc_indicator_ids,dwc_campaign_ids]))

        return ids_to_delete

    def file_to_source_submissions(self):

        batch = {}
        for submission in self.csv_df.itertuples():

            ss, instance_guid = self.process_raw_source_submission(submission)
            if ss is not None and instance_guid is not None:

                ss['instance_guid'] = instance_guid
                batch[instance_guid] = ss

        object_list = [SourceSubmission(**v) for k,v in batch.iteritems()]
        ss = SourceSubmission.objects.bulk_create(object_list)

        return
