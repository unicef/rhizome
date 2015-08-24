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


    def prep_file(self,full_file_path):

        f_header = open(full_file_path,'r')
        self.file_header = f_header.readlines()[0].split(self.file_delimiter)
        f_header.close()

        f = open(full_file_path,'r')
        file_stream = f.readlines()[1:]

        return file_stream

    def process_file(self):
        '''
        Returns a list of source submisison objects
        '''


        full_file_path = settings.MEDIA_ROOT + self.file_path
        file_stream = self.prep_file(full_file_path)
        file_row_count = len(file_stream)

        batch = []
        for i,(submission) in enumerate(file_stream):

            submission_data = dict(zip(self.file_header, \
                submission.split(self.file_delimiter)))

            instance_guid = submission_data['uq_id']

            if instance_guid != '': ## so as to not process empty rows

                submission_dict = {
                    'submission_json': submission_data,
                    'document_id': self.document_id,
                    'row_number': i,
                    'instance_guid': i,
                    'process_status': 'TO_PROCESS',
                }
                batch.append(SourceSubmission(**submission_dict))

        ss = SourceSubmission.objects.bulk_create(batch)

        return ss
