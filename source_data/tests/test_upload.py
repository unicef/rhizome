
import urllib
import pprint as pp
import os
from time import gmtime, strftime

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.auth.models import User

from source_data.views import file_upload
from source_data.models import Document

class UploadTestCase(TestCase):
    ''' various cases involved with xls and csv upload '''

    def setUp(self):

        self.user = User.objects.create_user(username='test_user',password='thepassword')

        self.client = Client()
        self.client.login(username='test_user',password='thepassword')
        self.source_static_root = '/Users/johndingee_seed/Desktop/polio_xls/'
        self.app_static_root = 'media/documents/'

        self.sample_txt = 'test_NG.txt'
        self.sample_xls = 'test_NG.xlsx'
        self.sample_csv = 'test_NG.csv'

        self.delete_test_files()


    def delete_test_files(self):
        for root, dirs, files in os.walk(self.app_static_root):

            for i,(file) in enumerate(files):
                if file.startswith('test_'):
                    full_path = os.path.join(root, file)
                    os.unlink(full_path)


    def doc_post(self):

        base_url = '/upload/file_upload/'

        with open(self.source_static_root + self.sample_xls) as doc:
            response = self.client.post(base_url, {'docfile': doc})

        expected_doc_path = 'documents/' + strftime("%Y/%m/%d/",gmtime()) + self.sample_xls

        request_doc_id = response.context['document_id']
        db_doc_id = Document.objects.get(docfile=expected_doc_path).id

        # ensure the doc ID is correct
        self.assertEqual(request_doc_id,db_doc_id)

        # is the proper user in the request?
        self.assertEqual(self.client.session['_auth_user_id'], self.user.pk)

    def test_doc_bad_file_ext(self):

        base_url = '/upload/file_upload/'

        with open(self.source_static_root + self.sample_txt) as doc:
            response = self.client.post(base_url, {'docfile': doc})

            msg = list(response.context['messages'])

        msg_text = msg[0].message
        expected_msg = 'Please upload either .CSV, .XLS or .XLSX file format'

        self.assertEqual(msg_text,expected_msg)
