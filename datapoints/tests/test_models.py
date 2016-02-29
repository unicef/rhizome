from django.test import TestCase
from datapoints.models import *
from datapoints.agg_tasks import AggRefresh
from datapoints.cache_meta import LocationTreeCache
from source_data.models import *
from datetime import datetime
from datetime import date, timedelta



class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        pass

class IndicatorTagTest(MasterModelTestCase):

    def set_up(self):
        self.tag_name = 'Ebola'
        create_tag = IndicatorTag.objects.create(tag_name = self.tag_name)

    def test_tag_create(self):

        self.set_up()
        ebola_tag = IndicatorTag.objects.get(tag_name = self.tag_name)

        self.assertEqual(ebola_tag.tag_name,self.tag_name)

    def test_get_indicator_ids_for_tag(self):

        self.set_up()
        test_tag = IndicatorTag.objects.get(tag_name = self.tag_name)

        ind_ds = test_tag.get_indicator_ids_for_tag()


class CampaignTest(MasterModelTestCase):

    # python manage.py test datapoints.tests.test_models.CampaignTest\
    #    .test_campaign_create --settings=rhizome.settings.test

    def set_up(self):

        self.d = date.today()
        st = self.d - timedelta(days=1)
        ed = self.d + timedelta(days=1)

        self.u = User.objects.create_user('polio','eradicate@polio.com', 'polio')
        o = Office.objects.create(name='NGA')
        lt = LocationType.objects.create(name='country',admin_level=0)
        ct = CampaignType.objects.create(name='NID')
        self.ind_0 = Indicator.objects.create(name='number of VDPV cases',short_name='V')
        self.ind_1 = Indicator.objects.create(name='number of WPV cases',short_name='W')
        ind_tag = IndicatorTag.objects.create(tag_name='Polio')
        self.tpl = Location.objects.create(name='NGA',location_code='NGA',\
            office_id = o.id,location_type_id = lt.id)
        self.doc = Document.objects.create(
            doc_title = 'test',
            created_by_id = self.u.id,
            guid = 'test')

        ### SET UP CAMPAIGN DEFINITION ###

        self.c = Campaign.objects.create(
            office_id = o.id,\
            top_lvl_location_id = self.tpl.id,
            top_lvl_indicator_tag_id = ind_tag.id,
            campaign_type_id = ct.id,
            name = 'test',\
            start_date = st,\
            end_date = ed,\
        )

        ltc = LocationTreeCache()
        ltc.main()

    def test_campaign_create_sets_cache_job_of_datapoints(self):

        self.set_up()

        start_date, data_date, end_date = '2018-01-01', '2018-01-10', '2018-01-31'

        print 'TOP LEVEL LOCATION ID:  %s' % self.tpl.id

        ss = SourceSubmission.objects.create(
            document_id = self.doc.id,
            submission_json = '',
            row_number = 0,
            data_date = self.d
        )
        dp = DataPoint.objects.create(
            id = 999999,
            location_id = self.tpl.id,\
            indicator_id = self.ind_0.id,\
            value=2,
            data_date = data_date,
            source_submission_id = ss.id,
            cache_job_id=-2
        )

        self.c.start_date = start_date
        self.c.end_date = end_date
        self.c.save() ## this should set the datapoint above to "to_process"

        dp_after_campaign_save = DataPoint.objects.get(id = dp.id)
        self.assertEqual(dp_after_campaign_save.cache_job_id, -1)

    def test_campaign_create(self):

        ###### ADD DATA TO CAMPAIGN #####

        self.set_up()

        ss = SourceSubmission.objects.create(
            document_id = self.doc.id,
            submission_json = '',
            row_number = 0,
            data_date = self.d
        )
        dp_0 = DataPoint.objects.create(
            location_id = self.tpl.id,\
            indicator_id = self.ind_0.id,\
            value=2,
            data_date = self.d,
            source_submission_id = ss.id,
            cache_job_id=-1
        )
        dp_1 = DataPoint.objects.create(\
            location_id = self.tpl.id,\
            indicator_id = self.ind_1.id,\
            value = 3,\
            data_date = self.d, \
            source_submission_id = ss.id,\
            cache_job_id = -1
        )

        agr = AggRefresh(campaign_id = self.c.id)

        dp_ids = self.c.get_datapoints()

        self.assertEqual(len(dp_ids),2)
        self.assertTrue(isinstance,(self.c,Campaign))
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

class DataPointTest(MasterModelTestCase):

    def set_up(self):

        self.user = User.objects.create(
            username='john')

        self.document = Document.objects.create(
            doc_title = 'test',
            created_by_id = self.user.id,
            guid = 'test')

    def create_datapoint(self, note="test", indicator_id=99, location_id = 99,
        value=100.01):

        self.set_up()

        source_submission = SourceSubmission.objects.create(
            document_id = self.document.id,
            submission_json = '',
            row_number = 1,
            data_date = '2016-01-01'
        )

        dp = DataPoint.objects.create(
            indicator_id=indicator_id,
            location_id = location_id,
            data_date='2016-01-01',
            value = value,
            source_submission_id = source_submission.id
            )

        return dp

    def test_datapoint_creation(self):

        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))

        # self.assertEqual(dp.__unicode__(),dp.value)
