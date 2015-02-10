from django.test import TestCase
from datapoints.models import *
from source_data.models import *


class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        set_up_dict = {}

        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        ##

        set_up_dict['user_id'] = User.objects.create(
            username='john').id

        ##

        set_up_dict['document_id'] = Document.objects.create(
            doc_text = 'test',
            created_by_id = set_up_dict['user_id'],
            guid = 'test').id


        return set_up_dict


class IndicatorTest(MasterModelTestCase):

    def test_datapoint_indicator_creation(self):

        set_up_dict = self.set_up()
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

    def create_region_type(self):

        region_type_id = RegionType.objects.create(name='test').id

        return region_type_id

    def create_region(self, name = "test", office_id=1):

        self.set_up()

        region_type_id = self.create_region_type()
        # source_region_id = self.create_source_region()

        region = Region.objects.create(name = name\
            ,office_id = office_id
            ,region_type_id = region_type_id\
            ,source_id = self.source.id)

        return region

    def test_region_creation(self):

        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.name)

        print '...Done Testing Region Model...'

class DataPointTest(MasterModelTestCase):

    def prep(self):

        self.status = ProcessStatus.objects.create(
            status_text = 'test',
            status_description = 'test')

        self.set_up_dict = self.set_up()


    def create_source_datapoint(self):

        self.prep()

        sdp_id = SourceDataPoint.objects.create(
            document_id = self.set_up_dict['document_id'],
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
