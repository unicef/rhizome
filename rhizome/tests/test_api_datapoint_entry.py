
"""
Data Point entry was split into two resoruces

date_datapoint, and campaign_datapoint

The test cases here are all valid, but the old datapointentry resource
has been depreciated.

The to do here is to adapt this test to act as the backbone for the new data
entry feature
"""

# from base_test_case import RhizomeApiTestCase
# from rhizome.tests.setup_helpers import TestSetupHelpers
# from rhizome.models import LocationPermission, CampaignType, IndicatorTag,\
#     DataPointEntry
#
# class DatapointEntryResourceTest(RhizomeApiTestCase):
#
#     def setUp(self):
#         super(DatapointEntryResourceTest, self).setUp()
#
#         self.ts = TestSetupHelpers()
#         self.lt = self.ts.create_arbitrary_location_type()
#         self.o = self.ts.create_arbitrary_office()
#
#         self.top_lvl_location = self.ts.create_arbitrary_location(
#             self.lt.id, self.o.id)
#
#         LocationPermission.objects.create(user_id=self.ts.user.id,
#                                           top_lvl_location_id=self.top_lvl_location.id)
#         self.ct = CampaignType.objects.create(name='NID')
#         self.it = IndicatorTag.objects.create(tag_name='Polio')
#
#         self.c = self.ts.create_arbitrary_campaign(
#             self.o.id, self.ct.id, self.top_lvl_location.id, self.it.id)
#         self.ind = self.ts.create_arbitrary_indicator()
#         self.doc = self.ts.create_arbitrary_document()
#         self.ss = self.ts.create_arbitrary_ss(self.doc.id)
#
#     def test_get(self):
#         dp = DataPointEntry.objects.create(
#             location_id=self.top_lvl_location.id,
#             data_date='2016-01-01',
#             indicator_id=self.ind.id,
#             value=1234,
#             cache_job_id=-1,
#             source_submission_id=self.ss.id,
#             campaign_id=self.c.id
#         )
#         data = {'campaign__in': self.c.id, 'indicator__in': self.ind.id}
#         resp = self.ts.get(self, '/api/v1/datapointentry/', data)
#         resp_data = self.deserialize(resp)
#         self.assertHttpOK(resp)
#         self.assertEqual(len(resp_data['objects']), 1)
#
#     def test_get_invalid_request(self):
#         data = {'campaign__in': 123, 'indicator__in': 456}
#         resp = self.ts.get(self, '/api/v1/datapointentry/', data)
#         self.assertHttpApplicationError(resp)
#
#     def test_post_new_dp(self):
#         dp_value = 4567
#         data = {
#             'campaign_id': self.c.id,
#             'location_id': self.top_lvl_location.id,
#             'indicator_id': self.ind.id,
#             'value': dp_value
#         }
#         resp = self.ts.post(self, '/api/v1/datapointentry/', data)
#         self.assertHttpCreated(resp)
#         resp_data = self.deserialize(resp)
#         self.assertEqual(resp_data['value'], dp_value)
#
#     # delete methods should fail
#     def test_delete(self):
#         dp = DataPointEntry.objects.create(
#             location_id=self.top_lvl_location.id,
#             data_date='2016-01-01',
#             indicator_id=self.ind.id,
#             value=1234,
#             cache_job_id=-1,
#             source_submission_id=self.ss.id,
#             campaign_id=self.c.id
#         )
#         self.assertEqual(DataPointEntry.objects.count(), 1)
#         delete_url = '/api/v1/datapointentry/?id=' + str(dp.id)
#         self.ts.delete(self, delete_url)
#         self.assertEqual(DataPointEntry.objects.count(), 1)
#
#     # what happens when we create a duplicate datapoint
#     def test_post_update_dp(self):
#         dp_value = 4567
#         data = {
#             'campaign_id': self.c.id,
#             'location_id': self.top_lvl_location.id,
#             'indicator_id': self.ind.id,
#             'value': dp_value
#         }
#         resp = self.ts.post(self, '/api/v1/datapointentry/', data)
#         self.assertHttpCreated(resp)
#         resp_data = self.deserialize(resp)
#         self.assertEqual(resp_data['value'], dp_value)
#
#         # do it again
#         new_val = 323
#         data['value'] = new_val
#         resp = self.ts.post(self, '/api/v1/datapointentry/', data)
#         self.assertHttpCreated(resp)
#         resp_data = self.deserialize(resp)
#
#         # make sure the api returns the new dp
#         data = {'campaign__in': self.c.id, 'indicator__in': self.ind.id}
#         get_resp = self.ts.get(self, '/api/v1/datapointentry/', data)
#         resp_data = self.deserialize(get_resp)
#         self.assertEqual(resp_data['objects'][0]['value'], new_val)
#
#     def test_post_invalid_campaign(self):
#         dp_value = 4567
#         data = {
#             'campaign_id': 1234,
#             'location_id': self.top_lvl_location.id,
#             'indicator_id': self.ind.id,
#             'value': dp_value
#         }
#         resp = self.ts.post(self, '/api/v1/datapointentry/', data)
#         self.assertHttpApplicationError(resp)
