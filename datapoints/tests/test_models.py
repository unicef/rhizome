from django.test import TestCase
from datapoints.models import *
from django.core.urlresolvers import reverse


class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        source_id = Source.objects.create(
            source_name = 'test',
            source_description = 'test').id

        return source_id





class IndicatorTest(MasterModelTestCase):


    def test_datapoint_indicator_creation(self):

        source_id = self.set_up()
        dpi = Indicator.objects.create(
            name = 'test',
            description = 'test',
            is_reported = 0,
            source_id = source_id
        )

        self.assertTrue(isinstance,(dpi,Indicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)

class RegionTest(MasterModelTestCase):

    def create_region_type(self):

        region_type_id = RegionType.objects.create(name='test')

        return region_type_id

    def create_region(self, name = "test", office_id=1):

        source_id = set_up
        region_type_id = create_region_type()


        return Region.objects.create(name=name,office_id=office_id)


    def test_region_creation(self):
        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.full_name)


class DataPointTest(MasterModelTestCase):

    def create_datapoint(self, note="test", indicator_id=99, region_id = 99,
        campaign_id=99, value=100.01, changed_by_id = 1):

        return DataPoint.objects.create(note=note, indicator_id=indicator_id,
         region_id = region_id, campaign_id=campaign_id,
         value=value,changed_by_id=changed_by_id)

        ## This should break on a foreign key violation but it doesnt!!

    def test_datapoint_creation(self):
        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))
        # self.assertEqual(dp.__unicode__(),dp.value)
