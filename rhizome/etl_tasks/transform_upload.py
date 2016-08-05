from pandas import read_csv
from pandas import notnull
from pandas import DataFrame

import json
from rhizome.api.exceptions import RhizomeApiException
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rhizome.models.document_models import Document

from datetime import datetime
from dateutil.parser import parse

class BadFileHeaderException(Exception):
    defaultMessage = "Your Header Has Commas in it, please fix and re-upload"
    defaultCode = -2


class DocTransform(object):


    def source_submission_meta_upsert(self, content_type, source_object_code):
        '''
        Create new metadata if not exists
        Add a record tying this document to the newly inserted metadata
        '''

        config_columns = [self.location_column, self.uq_id_column,
                          self.campaign_column, 'District', 'DCODE', 'District.Name',
                          'DCODE', 'level', 'PCODE', 'Province']

        if content_type == 'indicator' and source_object_code in config_columns:
            return  # so we dont think that "campaign" is an indicator

        # this is sketchy, but since there is no user when we do the initial
        # data migration, we have to set mapped_by_id = None
        upload_user_id = None
        if self.user_id > 0:
            upload_user_id = self.user_id

        sm_obj, created = SourceObjectMap.objects.get_or_create(
            content_type=content_type, source_object_code=str(source_object_code), defaults={
                'master_object_id': -1,
                'mapped_by_id': upload_user_id
            })

        sm_obj, created = DocumentSourceObjectMap.objects.get_or_create\
            (document_id=self.document.id, source_object_map_id=sm_obj.id)

        return sm_obj.id



class CampaignDocTransform(DocTransform):
    '''
    This type of transformation handles abstract data for which :
        date_column - refers to the date of the collected data
        location_column - refers to the location code f the collected data
        indicators - indicators are columns.
    '''

    def __init__(self, user_id, document_id, raw_csv_df=None):

        super(CampaignDocTransform, self).__init__(
            user_id, document_id, raw_csv_df)

        # if we allow for user input to choose column definitinos
        # we can pull the data frmo the below calls.  Since we are hard
        # coding configurations and expecting a upload template then
        # we dont need the belwo code.
        # self.uq_id_column = DocumentDetail.objects.get(
        #     document_id = self.document.id,
        #     doc_detail_type_id = DocDetailType\
        #         .objects.get(name='uq_id_column').id,
        # ).doc_detail_value
        #
        # self.location_column = str(DocumentDetail.objects.get(
        #     document_id = self.document.id,
        #     doc_detail_type_id = DocDetailType\
        #         .objects.get(name='location_column').id,
        # ).doc_detail_value)
        #
        # self.date_column = str(DocumentDetail.objects.get(
        #     document_id = self.document.id,
        #     doc_detail_type_id = DocDetailType\
        #         .objects.get(name='date_column').id,
        # ).doc_detail_value)

    def main(self):
        self.process_file()
        self.upsert_source_object_map()

    # def process_date_column(self, doc_df):
    #
    #     dt_col = to_datetime(doc_df[self.date_column])
    #     doc_df['data_date'] = dt_col
    #
    #     return doc_df



class DateDocTransform(DocTransform):

    def __init__(self, user_id, document_id, raw_csv_df=None):

        super(DateDocTransform, self).__init__(
            user_id, document_id, raw_csv_df)

    def process_raw_source_submission(self, submission):

        submission_ix, submission_data = submission[0], submission[1:]

        submission_data = dict(zip(self.file_header, submission_data))
        instance_guid = submission_data[self.uq_id_column]

        if instance_guid == '' or instance_guid in self.existing_submission_keys:
            return None, None

        cleaned_date = parse(submission_data['data_date'])
        submission_dict = {
            'submission_json': submission_data,
            'document_id': self.document.id,
            'row_number': submission_ix,
            'location_code': submission_data[self.location_column],
            'data_date': cleaned_date,
            'instance_guid': submission_data[self.uq_id_column],
            'process_status': 'TO_PROCESS',
        }
        return submission_dict, instance_guid


    def main(self):
        self.document_to_source_submission()

    def document_to_source_submission(self):
        '''
        Takes a file and dumps the data into the source submission table.
        Returns a list of source_submission_ids
        '''

        # full_file_path = settings.MEDIA_ROOT + self.file_path
        # raw_csv_df = read_csv(full_file_path)
        # csv_df = raw_csv_df.where((notnull(raw_csv_df)), None)

        ## transform the raw data based on the documents configurations ##
        doc_df = self.apply_doc_config_to_csv_df(self.csv_df)
        # doc_df = self.process_date_column(doc_df)

        doc_obj = Document.objects.get(id=self.document.id)
        doc_obj.file_header = list(doc_df.columns.values)
        doc_obj.save()

        self.file_header = doc_obj.file_header

        batch = {}

        for submission in doc_df.itertuples():

            ss, instance_guid = self.process_raw_source_submission(submission)

            if ss is not None and instance_guid is not None:
                ss['instance_guid'] = instance_guid
                batch[instance_guid] = ss

        object_list = [SourceSubmission(**v) for k, v in batch.iteritems()]
        ss = SourceSubmission.objects.bulk_create(object_list)
        return [x.id for x in ss]

    def apply_doc_config_to_csv_df(self, csv_df):
        '''
        Currenlty this only applies to the 'Location Code Column Length'
        configuration which allows us to ingest the ODK data at the one level
        higher than it is collected.
        This is a short term solution, but saves us massive ammounts of work
        in Mapping, and also makes it such that we don't need to create location
        IDs for the 10k settlements in Nigeria.
        '''

        try:
            location_code_column_length = int(DocumentDetail.objects.get(
                document_id=self.document.id,
                doc_detail_type_id=DocDetailType.objects.get(
                    name='Location Code Column Length')
            ).doc_detail_value)

            ## truncate the location_codes in accordance to the value above ##
            csv_df[self.location_column] = csv_df[self.location_column]\
                .apply(lambda x: str(x)[:location_code_column_length])

        except ObjectDoesNotExist:
            pass

        return csv_df
