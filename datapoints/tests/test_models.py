from django.test import TestCase
from datapoints.models import DataPointIndicator, Region, DataPoint
from django.core.urlresolvers import reverse


class DataPointIndicatorTest(TestCase):

    def create_data_point_indicator(self, name="test", description = "dtest"):
        return DataPointIndicator.objects.create(name=name,description=description)

    def test_datapoint_indicator_createion(self):
        dpi = self.create_data_point_indicator()
        self.assertTrue(isinstance,(dpi,DataPointIndicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)

class RegionTest(TestCase):

    def create_region(self, full_name="test", short_name = "short test"):
        return Region.objects.create(full_name=full_name,short_name=short_name)

    def test_datapoint_indicator_createion(self):
        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.short_name)

class DataPointTest(TestCase):

    def create_datapoint(self, note="test", indicator_id=99, region_id = 99, value=100.01):
        return DataPoint.objects.create(note=note, indicator_id=indicator_id, region_id = region_id, value=value)
        ## This should break on a foreign key violation but it doesnt!!

    def test_datapoint_createion(self):
        dp = self.create_datapoint()
        self.assertTrue(isinstance,(dp,DataPoint))
        # self.assertEqual(dp.__unicode__(),dp.value.__un)
