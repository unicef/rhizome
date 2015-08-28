from pandas import read_csv
from pandas import notnull
from pprint import pprint

from django.conf import settings
from django.db import transaction
from pandas.io.excel import read_excel

from source_data.models import *
from datapoints.models import DataPoint


class DocTransform(object):

    def __init__(self,document_id,file_path=None):

        self.source_datapoints = []
        self.document_id = document_id

        ## SHOULD BE USER INPUT AND STORED IN DOC_DETAIL ##
        self.file_delimiter = ','

        if not file_path:
            file_path = str(Document.objects.get(id=self.document_id).\
                docfile)

        self.file_path = file_path

        self.to_process_status = ProcessStatus.objects.\
            get(status_text='TO_PROCESS').id


    def pre_process_file(self,full_file_path):

        f_header = open(full_file_path,'r')
        top_row = f_header.readlines()[0]
        cleaned = top_row.replace('\r','').replace('\n','')
        self.file_header = cleaned.split(self.file_delimiter)

        f_header.close()

        f = open(full_file_path,'r')
        file_stream = f.readlines()[1:]

        return file_stream

    def post_process_file(self):
        '''
        Put the submission data into a clean table for the view_raw section
        of the source data management app.
        '''

        username_column = DocumentDetail.objects.get(
            document_id = self.document_id,
            doc_detail_type_id = DocDetailType.objects.get(name=\
                'username_column').id
        ).doc_detail_value

        image_col = DocumentDetail.objects.get(
            document_id = self.document_id,
            doc_detail_type_id = DocDetailType.objects.get(name='image_col').id
        ).doc_detail_value

        source_submissions = SourceSubmission.objects.filter(document_id = \
            self.document_id)

        batch = []
        for i, (row) in enumerate(source_submissions):

            submission_data = row.submission_json
            submission_detail_dict = {
                'source_submission_id': row.id,
                'img_location':  submission_data[image_col],
                'document_id':   self.document_id,
                'submission_username':  submission_data[username_column],
            }
            batch.append(SourceSubmissionDetail(**submission_detail_dict))

        # remove this delete #
        SourceSubmissionDetail.objects.all().delete()
        SourceSubmissionDetail.objects.bulk_create(batch)

        return []

    def process_file(self):
        '''
        Returns a list of source submisison objects
        '''

        full_file_path = settings.MEDIA_ROOT + self.file_path
        file_stream = self.pre_process_file(full_file_path)
        file_row_count = len(file_stream)

        doc_detail_type_id = DocDetailType.objects.get(name='uq_id_column').id
        uq_id_column = DocumentDetail.objects.get(
            document_id = self.document_id,
            doc_detail_type_id = doc_detail_type_id
        ).doc_detail_value

        batch = []
        for i,(submission) in enumerate(file_stream):

            submission_data = dict(zip(self.file_header, \
                submission.split(self.file_delimiter)))

            submission_dict = {
                'submission_json': submission_data,
                'document_id': self.document_id,
                'row_number': i,
                'instance_guid': submission_data[uq_id_column],
                'process_status': 'TO_PROCESS',
            }
            batch.append(SourceSubmission(**submission_dict))

        ## FIXME this delete is for testing .. REMOVE!
        SourceSubmission.objects.filter(document_id=self.document_id).delete()
        ss = SourceSubmission.objects.bulk_create(batch)

        to_return = self.post_process_file()

        return ss
