from django.test import TestCase
from datapoints.models import Indicator, Region, DataPoint
from django.core.urlresolvers import reverse


class IndicatorTest(TestCase):

    def create_indicator(self, name="test", description = "dtest"):
        return Indicator.objects.create(name=name,description=description)

    def test_datapoint_indicator_creation(self):
        dpi = self.create_indicator()
        self.assertTrue(isinstance,(dpi,Indicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)

class RegionTest(TestCase):

    def create_region(self, full_name = "full test", office_id=1):
        return Region.objects.create(full_name=full_name,office_id=office_id)

    def test_region_creation(self):
        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.full_name)

class DataPointTest(TestCase):

    def create_datapoint(self, note="test", indicator_id=99, region_id = 99,
        campaign_id=99, value=100.01, changed_by_id = 1):

        return DataPoint.objects.create(note=note, indicator_id=indicator_id,
         region_id = region_id, campaign_id=campaign_id,
         value=value,changed_by_id=changed_by_id)

        ## This should break on a foreign key violation but it doesnt!!

    def test_datapoint_createion(self):
        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))
        # self.assertEqual(dp.__unicode__(),dp.value)
