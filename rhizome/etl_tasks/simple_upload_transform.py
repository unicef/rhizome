import json
import math

from pandas import read_csv, DataFrame
from pandas import notnull
from django.conf import settings

from rhizome.models import SourceObjectMap, DocumentSourceObjectMap, SourceSubmission, DataPointComputed
from rhizome.api.exceptions import DatapointsException
from rhizome.etl_tasks.transform_upload import DocTransform
from django.db import IntegrityError


class SimpleDocTransform(DocTransform):
    '''
    Based on a very specific pre/intra/post campaign template, we sync data
    and don't ask questions.
    '''

    def __init__(self, user_id, document_id):

        return super(SimpleDocTransform, self).__init__(user_id, document_id)

    def build_meta_lookup(self):

        csv_location_codes = list(self.csv_df[self.location_column].unique())
        csv_campaign_codes = list(self.csv_df[self.campaign_column].unique())

        location_lookup = SourceObjectMap.objects\
            .filter(content_type='location',
                    source_object_code__in=csv_location_codes)\
            .values_list('source_object_code', 'master_object_id')

        for source_object_code, master_object_id in location_lookup:
            self.meta_lookup['location'][source_object_code] = master_object_id

        ## build campaign lookup ##
        campaign_lookup = SourceObjectMap.objects\
            .filter(content_type='campaign',
                    source_object_code__in=csv_campaign_codes)\
            .values_list('source_object_code', 'master_object_id')

        for source_object_code, campaign_id in campaign_lookup:
            self.meta_lookup['campaign'][source_object_code] = campaign_id

        ## build indicator lookup ##
        indicator_lookup = SourceObjectMap.objects\
            .filter(content_type='indicator',
                    source_object_code__in=self.file_header)\
            .values_list('source_object_code', 'master_object_id')

        for source_object_code, indicator_id in indicator_lookup:
            if indicator_id in self.meta_lookup['indicator'].values():
                self.indicator_ids_to_exclude.add(indicator_id)
            self.meta_lookup['indicator'][source_object_code] = indicator_id

    def main(self):

        ## only ingest submissions and upsert meta data if this is the first  ##
        ## time the document is being processed ##
        if not DocumentSourceObjectMap.objects.filter(document_id=self.document.id):
            self.file_to_source_submissions()
            self.upsert_source_object_map()

        self.build_meta_lookup()

        all_data, all_unique_keys = [], []
        for row in SourceSubmission.objects.filter(document_id=self.document.id):
            row_batch, dwc_list_of_lists = self.process_source_submission(row)
            if row_batch:
                all_data.extend(row_batch)
                all_unique_keys.extend(dwc_list_of_lists)

        dwc_ids_to_delete = self.get_dwc_ids_to_delete(all_unique_keys)
        DataPointComputed.objects.filter(id__in=dwc_ids_to_delete).delete()
        DataPointComputed.objects.bulk_create(all_data)

    def process_raw_source_submission(self, submission):

        submission_ix, submission_data = submission[0], submission[1:]

        submission_data = dict(zip(self.file_header, submission_data))
        instance_guid = submission_data[self.uq_id_column]

        if type(instance_guid) == float and math.isnan(instance_guid):
            return None, None

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

    def process_source_submission(self, row):

        dwc_batch, dwc_list_of_lists = [], []
        submission = row.submission_json

        try:
            location_id = self.meta_lookup['location'][row.location_code]
            campaign_id = self.meta_lookup['campaign'][row.campaign_code]
        except KeyError:
            None, None

        if location_id == -1 or campaign_id == -1:
            return None, None

        for k, v in submission.iteritems():

            dwc_obj, indicator_id = self.process_submission_cell(
                location_id, campaign_id, k, v)

            if dwc_obj:
                dwc_batch.append(dwc_obj)
                dwc_list_of_lists.append(
                    [location_id, indicator_id, campaign_id])

        return dwc_batch, dwc_list_of_lists

    def process_submission_cell(self, location_id, campaign_id, k, v):
        value_lookup = {'yes': 1, 'no': 0, 'Yes': 1, 'No': 0, '': None}

        try:
            looked_up_val = value_lookup[v]
        except KeyError:
            looked_up_val = v

        try:
            indicator_id = self.meta_lookup['indicator'][k]

        except KeyError:
            return None, None

        if indicator_id in self.indicator_ids_to_exclude:
            return None, None

        if v is None:
            return None, None

        try:
            float_val = float(v)
        except ValueError:
            return None, None

        if indicator_id:
            dwc_obj = DataPointComputed(**{
                'location_id': location_id,
                'indicator_id': indicator_id,
                'campaign_id': campaign_id,
                'value': float_val,
                'cache_job_id': -1,
                'document_id': self.document.id
            })
            return dwc_obj, indicator_id

    def get_dwc_ids_to_delete(self, dwc_list_of_lists):

        df = DataFrame(dwc_list_of_lists, columns=['location_id',
                                                   'indicator_id', 'campaign_id'])

        uq_location_id_list = list(df['location_id'].unique())
        uq_indicator_id_list = list(df['indicator_id'].unique())
        uq_campaign_id_list = list(df['campaign_id'].unique())

        dwc_location_ids = DataPointComputed.objects.filter(
            location_id__in=uq_location_id_list).values_list('id', flat=True)

        dwc_indicator_ids = DataPointComputed.objects.filter(
            indicator_id__in=uq_indicator_id_list).values_list('id', flat=True)

        dwc_campaign_ids = DataPointComputed.objects.filter(
            campaign_id__in=uq_campaign_id_list).values_list('id', flat=True)

        ids_to_delete = set.intersection(*map(set,
                                              [dwc_location_ids, dwc_indicator_ids, dwc_campaign_ids]))

        return ids_to_delete

    def file_to_source_submissions(self):
        # use a dictionary to make sure that there is a single value for each instance_guid.
        # duplicates are handled by overwriting old values
        batch = {}
        for submission in self.csv_df.itertuples():

            ss, instance_guid = self.process_raw_source_submission(submission)
            if ss is not None and instance_guid is not None:
                ss['instance_guid'] = instance_guid
                batch[instance_guid] = ss

        object_list = [SourceSubmission(**v) for k, v in batch.iteritems()]

        try:
            ss = SourceSubmission.objects.bulk_create(object_list)
        except IntegrityError as e:
            raise DatapointsException(e.message)

        return
