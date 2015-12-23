from django.test import TestCase
from datapoints.models import *
from datapoints.agg_tasks import AggRefresh
from source_data.models import *
from datetime import datetime

class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        pass


class CampaignTest(MasterModelTestCase):

    # python manage.py test datapoints.tests.test_models.CampaignTest\
    #    .test_campaign_create --settings=rhizome.settings.test

    def test_campaign_create(self):

        u = User.objects.create_user('polio','eradicate@polio.com', 'polio')
        o = Office.objects.create(name='NGA')
        lt = LocationType.objects.create(name='country',admin_level=0)
        ct = CampaignType.objects.create(name='NID')
        ind_0 = Indicator.objects.create(name='number of VDPV cases',short_name='V')
        ind_1 = Indicator.objects.create(name='number of WPV cases',short_name='W')
        tpl = Location.objects.create(name='NGA',location_code='NGA',\
            office_id = o.id,location_type_id = lt.id)
        doc = Document.objects.create(
            doc_title = 'test',
            created_by_id = u.id,
            guid = 'test')

        ss = SourceSubmission.objects.create(
            document_id = doc.id,
            submission_json = '',
            row_number = 0
        )

        ##
        c = Campaign.objects.create(
            office_id = o.id,\
            top_lvl_location_id = tpl.id,
            campaign_type_id = ct.id,
            name = 'test',\
            start_date = '2016-01-01',\
            end_date = '2016-01-01',\
        )

        dp_0 = DataPoint.objects.create(campaign_id=c.id,location_id=tpl.id,\
            indicator_id=ind_0.id,value=2,data_date = datetime.now(),
            changed_by_id = u.id,source_submission_id = ss.id)
        dp_1 = DataPoint.objects.create(campaign_id=c.id,location_id=tpl.id,\
            indicator_id=ind_1.id,value=3,data_date = datetime.now(), \
            changed_by_id = u.id,source_submission_id = ss.id)

        # agr = AggRefresh()
        # agr.main()

        dp_ids = c.get_datapoints()

        self.assertEqual(len(dp_ids),2)
        self.assertTrue(isinstance,(c,Campaign))
        # self.assertEqual(dpi.__unicode__(),dpi.name)

class IndicatorTest(MasterModelTestCase):

    def test_datapoint_indicator_creation(self):

        self.set_up()

        dpi = Indicator.objects.create(
            name = 'test',
            description = 'test',
            is_reported = 0)

        self.assertTrue(isinstance,(dpi,Indicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)


class LocationTest(MasterModelTestCase):

    def set_up(self):

        self.location_type_id = LocationType.objects.create(name='test',admin_level=0).id

    def create_location(self, name = "test", office_id=1):

        self.set_up()

        location = Location.objects.create(name = name\
            ,office_id = office_id
            ,location_type_id = self.location_type_id)

        return location

    def test_location_creation(self):

        r = self.create_location()
        self.assertTrue(isinstance,(r,Location))
        self.assertEqual(r.__unicode__(),r.name)

        print '...Done Testing location Model...'

class DataPointTest(MasterModelTestCase):

    def set_up(self):

        self.status = ProcessStatus.objects.create(
            status_text = 'test',
            status_description = 'test')

        self.user = User.objects.create(
            username='john')

        self.document = Document.objects.create(
            doc_title = 'test',
            created_by_id = self.user.id,
            guid = 'test')

    def create_datapoint(self, note="test", indicator_id=99, location_id = 99,
        campaign_id=99, value=100.01, changed_by_id = 1):

        self.set_up()

        source_submission = SourceSubmission.objects.create(
            document_id = self.document.id,
            submission_json = '',
            row_number = 1
        )

        dp = DataPoint.objects.create(
            indicator_id=indicator_id,
            location_id = location_id,
            campaign_id=campaign_id,
            value = value,
            changed_by_id=changed_by_id,
            source_submission_id = source_submission.id
            )

        return dp

    def test_datapoint_creation(self):

        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))

        # self.assertEqual(dp.__unicode__(),dp.value)
