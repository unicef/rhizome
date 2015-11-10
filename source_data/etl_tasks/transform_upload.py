from pandas import read_csv
from pandas import notnull
import json

from django.conf import settings

from source_data.models import * 

class BadFileHeaderException(Exception):
    defaultMessage = "Your Header Has Commas in it, please fix and re-upload"
    defaultCode = -2


class DocTransform(object):

    def __init__(self,user_id,document_id):

        self.source_datapoints = []
        self.user_id = user_id
        self.document = Document.objects.get(id=document_id)

        ## SHOULD BE USER INPUT AND STORED IN DOC_DETAIL ##
        self.file_delimiter = ','

        self.file_path = str(Document.objects.get(id=self.document.id).\
            docfile)

        self.to_process_status = ProcessStatus.objects.\
            get(status_text='TO_PROCESS').id

        self.uq_id_column = DocumentDetail.objects.get(
            document_id = self.document.id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='uq_id_column').id,
        ).doc_detail_value

        self.location_column = str(DocumentDetail.objects.get(
            document_id = self.document.id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='location_column').id,
        ).doc_detail_value)

        self.campaign_column = str(DocumentDetail.objects.get(
            document_id = self.document.id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='campaign_column').id,
        ).doc_detail_value)

        self.existing_submission_keys = SourceSubmission.objects.filter(
            document_id = self.document.id
        ).values_list('instance_guid',flat=True)

    def main(self):

        self.process_file()
        self.upsert_source_object_map()

    def process_file(self):
        '''
        Takes a file and dumps the data into the source submission table.

        Returns a list of source_submission_ids
        '''

        full_file_path = settings.MEDIA_ROOT + self.file_path
        raw_csv_df = read_csv(full_file_path)
        csv_df = raw_csv_df.where((notnull(raw_csv_df)), None)

        doc_obj = Document.objects.get(id = self.document.id)
        doc_obj.file_header = list(csv_df.columns.values)
        doc_obj.save()

        ## this probably break the test..shoudl see if i can get this in init ##
        self.file_header = doc_obj.file_header

        batch = {}

        for submission in csv_df.itertuples():

            ss, instance_guid = self.process_raw_source_submission(submission)

            if ss is not None and instance_guid is not None:
                ss['instance_guid'] = instance_guid
                batch[instance_guid] = ss

        object_list = [SourceSubmission(**v) for k,v in batch.iteritems()]
        ss = SourceSubmission.objects.bulk_create(object_list)

        return [x.id for x in ss]


    def upsert_source_object_map(self):
        '''
        TODO: save the source_strings so i dont have to iterate through
        the source_submission json.

        endpoint: api/v2/doc_mapping/?document=66
        '''

        source_dp_json = SourceSubmission.objects.filter(
            document_id = self.document.id).values_list('submission_json')

        if len(source_dp_json) == 0:
            return

        all_codes = [('indicator',k) for k,v in json.loads(source_dp_json[0][0]).iteritems()]
        rg_codes, cp_codes = [],[]

        for row in source_dp_json:
            row_dict = json.loads(row[0])

            rg_codes.append(row_dict[self.location_column])
            cp_codes.append(row_dict[self.campaign_column])

        for r in list(set(rg_codes)):
            all_codes.append(('location',r))

        for c in list(set(cp_codes)):
            all_codes.append(('campaign',c))

        for content_type, source_object_code in all_codes:
            self.source_submission_meta_upsert(content_type, source_object_code)

    def source_submission_meta_upsert(self, content_type, source_object_code):
        '''
        Create new metadata if not exists
        Add a record tying this document to the newly inserted metadata
        '''


        sm_obj, created = SourceObjectMap.objects.get_or_create(\
            content_type = content_type\
           ,source_object_code = str(source_object_code)\
           ,defaults = {
            'master_object_id':-1,
            'mapped_by_id':self.user_id
            })

        sm_obj, created = DocumentSourceObjectMap.objects.get_or_create\
            (document_id = self.document.id,source_object_map_id = sm_obj.id)

        return sm_obj.id


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
