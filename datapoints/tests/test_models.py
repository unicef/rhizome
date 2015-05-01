from django.test import TestCase
from datapoints.models import *
from source_data.models import *


class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.user = User.objects.create(
            username='john')

        self.document = Document.objects.create(
            doc_text = 'test',
            created_by_id = self.user.id,
            guid = 'test')


class IndicatorTest(MasterModelTestCase):

    def test_datapoint_indicator_creation(self):

        self.set_up()

        dpi = Indicator.objects.create(
            name = 'test',
            description = 'test',
            is_reported = 0,
            source_id = self.source.id)

        self.assertTrue(isinstance,(dpi,Indicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)

        print '...Done Testing Indicator Model...'


class RegionTest(MasterModelTestCase):

    def set_up(self):

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.region_type_id = RegionType.objects.create(name='test').id

    def create_region(self, name = "test", office_id=1):

        self.set_up()

        # source_id = self.create_source_region()

        region = Region.objects.create(name = name\
            ,office_id = office_id
            ,region_type_id = self.region_type_id\
            ,source_id = self.source.id)

        return region

    def test_region_creation(self):

        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.name)

        print '...Done Testing Region Model...'

class DataPointTest(MasterModelTestCase):

    def set_up(self):

        self.status = ProcessStatus.objects.create(
            status_text = 'test',
            status_description = 'test')

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.user = User.objects.create(
            username='john')

        self.document = Document.objects.create(
            doc_text = 'test',
            created_by_id = self.user.id,
            guid = 'test')

    def create_source_datapoint(self):

        self.set_up()

        sdp_id = SourceDataPoint.objects.create(
            document_id = self.document.id,
            row_number = 0,
            source_id =self.source.id,
            status_id = self.status.id).id


        return sdp_id


    def create_datapoint(self, note="test", indicator_id=99, region_id = 99,
        campaign_id=99, value=100.01, changed_by_id = 1):

        sdp_id = self.create_source_datapoint()

        dp = DataPoint.objects.create(
            indicator_id=indicator_id,
            region_id = region_id,
            campaign_id=campaign_id,
            value = value,
            changed_by_id=changed_by_id,
            source_datapoint_id = sdp_id,
            )

        return dp

    def test_datapoint_creation(self):

        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))
        print '....Done Testing DataPoint Model...'

        # self.assertEqual(dp.__unicode__(),dp.value)
