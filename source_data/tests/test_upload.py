import urllib

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.auth.models import User

from source_data.views import file_upload

class UploadTestCase(TestCase):
    ''' various cases involved with xls and csv upload '''

    def setUp(self):

        self.user = User.objects.create_user(username='test_user',password='thepassword')

        self.client = Client()
        self.client.login(username='test_user',password='thepassword')

        self.sample_xls = '/Users/johndingee_seed/Desktop/polio_xls/NG_2014_04.xlsx'
        self.sample_csv = '/Users/johndingee_seed/Desktop/polio_xls/NG_2014_04.csv'

    ## test the view
        ## csv or xls

    ## test bogus region, campaign, columns


    def test_something(self):

        base_url = '/upload/file_upload/'


        with open(self.sample_xls) as doc:
            response = self.client.post(base_url, {'docfile': doc})


        #     print '=\n' * 10
        #     response_user =  response.context['user']
        #     print type(response_user)
        #
        #     print response_user
        #
        # self.assertEqual(1,1)
