import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from setup_helpers import TestSetupHelpers
from pandas import read_csv, notnull, to_datetime
from rhizome.models import *

class DatapointEntryResourceTest(ResourceTestCase):
    def setUp(self):
        super(DatapointEntryResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(self.lt.id, self.o.id)

        LocationPermission.objects.create(user_id = self.ts.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)
        self.ct = CampaignType.objects.create(name='NID')
        self.it = IndicatorTag.objects.create(tag_name='Polio')

        self.c = self.ts.create_arbitrary_campaign(self.o.id, self.ct.id, self.top_lvl_location.id, self.it.id)
        self.ind = self.ts.create_arbitrary_indicator()
        self.doc = self.ts.create_arbitrary_document()
        self.ss = self.ts.create_arbitrary_ss(self.doc.id)

    def test_get(self):
        dp = DataPointEntry.objects.create(
            location_id = self.top_lvl_location.id,
            data_date = '2016-01-01',
            indicator_id = self.ind.id,
            value = 1234,
            cache_job_id = -1,
            source_submission_id = self.ss.id
        )
        data = {'campaign__in': self.ct.id, 'indicator__in': self.ind.id}
        resp = self.ts.get(self, '/api/v1/datapointentry/', data)
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 1)


    def test_get_invalid_request(self):
        data = {'campaign__in': 123, 'indicator__in': 456}
        resp = self.ts.get(self, '/api/v1/datapointentry/', data)
        self.assertHttpApplicationError(resp)

    # def test_post_new_dp(self):
    #     data={
    #     'campaign_id': self.top_lvl_location.id,
    #     'indicator_id': self.ind.id,
    #     'value': 4567
    #     }

    #     resp = self.ts.post(self, '/api/v1/datapointentry/', data)
    #     print(resp)


