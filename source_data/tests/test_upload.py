import urllib

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.contrib.auth.models import User

from source_data.views import file_upload

class UploadTestCase(TestCase):
    ''' various cases involved with xls and csv upload '''

    def setUp(self):
        self.sample_xls = '/Users/johndingee_seed/Desktop/polio_xls/NG_2014_04.xlsx'
        self.sample_csv = '/Users/johndingee_seed/Desktop/polio_xls/NG_2014_04.csv'
        self.user = User.objects.create(username='test_user')

    ## test the view
        ## csv or xls

    ## test bogus region, campaign, columns


    def test_something(self):

        client = Client()
        base_url = '/upload/file_upload/'



        with open(self.sample_xls) as doc:
            response = client.post(base_url, {'docfile': doc, 'user': self.user})

            print '=\n' * 10
            response_user =  response.context['user']
            print type(response_user)

            print response_user

        self.assertEqual(1,1)
