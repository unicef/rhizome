from tastypie.test import ResourceTestCase
from setup_helpers import TestSetupHelpers
from rhizome.models import Document, DocDataPoint, Indicator, CampaignType, IndicatorTag

class DocDataPointResourceTest(ResourceTestCase):
    def setUp(self):

        ## instantiate the test client and all other methods ##
        super(DocDataPointResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()
        self.top_lvl_location = self.ts.create_arbitrary_location(
            self.lt.id,
            self.o.id,
            location_code ='Nigeria',
            location_name='Nigeria')

    def test_doc_dp_get(self):
    	doc = Document.objects.create(doc_title="test")
    	camp_type = CampaignType.objects.create(name="test")
    	ind_tag = IndicatorTag.objects.create(tag_name="tag")
    	campaign = self.ts.create_arbitrary_campaign(self.o.id, camp_type.id, self.top_lvl_location.id, ind_tag.id)
    	ind = self.ts.create_arbitrary_indicator()
    	value = 1123
    	doc_dp = DocDataPoint.objects.create(document_id = doc.id,\
    		indicator_id =ind.id,
    		location_id = self.top_lvl_location.id,
    		campaign_id =campaign.id,
    		value=value,
    		source_submission_id=2,
    		agg_on_location=False )
    	data = {'document_id':doc.id}
    	url = '/api/v1/doc_datapoint/'
        resp = self.ts.get(self, url, data=data)
        response_data = self.deserialize(resp)
        self.assertHttpOK(resp)
        self.assertEqual(response_data['objects'][0]['value'], value)

