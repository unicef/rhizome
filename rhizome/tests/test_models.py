from django.test import TestCase

from django.contrib.auth.models import User

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign, CampaignType
from rhizome.models.location_models import Location, LocationType
from rhizome.models.indicator_models import Indicator, IndicatorTag
from rhizome.models.document_models import Document, SourceSubmission, \
    DataPoint

from rhizome.cache_meta import LocationTreeCache
from datetime import date, timedelta


class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        pass


class IndicatorTagTest(MasterModelTestCase):

    def set_up(self):
        self.tag_name = 'Ebola'
        create_tag = IndicatorTag.objects.create(tag_name=self.tag_name)

    def test_tag_create(self):

        self.set_up()
        ebola_tag = IndicatorTag.objects.get(tag_name=self.tag_name)

        self.assertEqual(ebola_tag.tag_name, self.tag_name)

class CampaignTest(MasterModelTestCase):

    # python manage.py test rhizome.tests.test_models.CampaignTest\
    #    .test_campaign_create --settings=rhizome.settings.test

    def set_up(self):

        self.d = date.today()
        st = self.d - timedelta(days=1)
        ed = self.d + timedelta(days=1)

        self.u = User.objects.create_user(
            'polio', 'eradicate@polio.com', 'polio')
        o = Office.objects.create(name='NGA')
        lt = LocationType.objects.create(name='country', admin_level=0)
        ct = CampaignType.objects.create(name='NID')
        self.ind_0 = Indicator.objects.create(
            name='number of VDPV cases', short_name='V')
        self.ind_1 = Indicator.objects.create(
            name='number of WPV cases', short_name='W')
        ind_tag = IndicatorTag.objects.create(tag_name='Polio')
        self.tpl = Location.objects.create(name='NGA', location_code='NGA',
                                           office_id=o.id, location_type_id=lt.id)
        self.doc = Document.objects.create(
            doc_title='test',
            created_by_id=self.u.id,
            guid='test')

        ### SET UP CAMPAIGN DEFINITION ###

        self.c = Campaign.objects.create(
            office_id=o.id,
            top_lvl_location_id=self.tpl.id,
            top_lvl_indicator_tag_id=ind_tag.id,
            campaign_type_id=ct.id,
            name='test',
            start_date=st,
            end_date=ed,
        )

        ltc = LocationTreeCache()
        ltc.main()


class IndicatorTest(MasterModelTestCase):

    def test_datapoint_indicator_creation(self):

        self.set_up()

        dpi = Indicator.objects.create(
            name='test',
            description='test',
            is_reported=0)

        self.assertTrue(isinstance, (dpi, Indicator))
        self.assertEqual(dpi.__unicode__(), dpi.name)


class LocationTest(MasterModelTestCase):

    def set_up(self):

        self.location_type_id = LocationType.objects.create(
            name='test', admin_level=0).id

    def create_location(self, name="test", office_id=1):

        self.set_up()

        location = Location.objects.create(
            name=name, office_id=office_id, location_type_id=self.location_type_id)

        return location

    def test_location_creation(self):

        r = self.create_location()
        self.assertTrue(isinstance, (r, Location))
        self.assertEqual(r.__unicode__(), r.name)


class DataPointTest(MasterModelTestCase):

    def set_up(self):

        self.user = User.objects.create(
            username='john')

        self.document = Document.objects.create(
            doc_title='test',
            created_by_id=self.user.id,
            guid='test')

    def create_datapoint(self, note="test", indicator_id=99, location_id=99, campaign_id=1, value=100.01):

        self.set_up()

        source_submission = SourceSubmission.objects.create(
            document_id=self.document.id,
            submission_json='',
            row_number=1,
            data_date='2016-01-01'
        )

        dp = DataPoint.objects.create(
            indicator_id=indicator_id,
            location_id=location_id,
            campaign_id=campaign_id,
            data_date='2016-01-01',
            value=value,
            source_submission_id=source_submission.id
        )

        return dp

    def test_datapoint_creation(self):

        dp = self.create_datapoint()
        self.assertTrue(isinstance, (dp, DataPoint))

        # self.assertEqual(dp.__unicode__(),dp.value)
