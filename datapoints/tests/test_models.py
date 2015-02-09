from django.test import TestCase
from datapoints.models import *
from source_data.models import *
from django.core.urlresolvers import reverse


class MasterModelTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(MasterModelTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        set_up_dict = {}

        set_up_dict['source_id'] = Source.objects.create(
            source_name = 'test',
            source_description = 'test').id

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
            source_id = set_up_dict['source_id']
        )

        self.assertTrue(isinstance,(dpi,Indicator))
        self.assertEqual(dpi.__unicode__(),dpi.name)

class RegionTest(MasterModelTestCase):


    def prep(self):

        self.set_up_dict = self.set_up()


    def create_region_type(self):

        region_type_id = RegionType.objects.create(name='test').id

        return region_type_id

    def create_source_region(self):

        self.prep()

        source_region_id = SourceRegion.objects.create(
            region_string = 'hello',
            document_id = self.set_up_dict['document_id']).id

        return source_region_id


    def create_region(self, name = "test", office_id=1):

        region_type_id = self.create_region_type()
        source_region_id = self.create_source_region()

        region = Region.objects.create(name = name\
            ,office_id = office_id
            ,region_type_id = region_type_id\
            ,source_id = self.set_up_dict['source_id']
            ,source_region_id = source_region_id)

        return region


    def test_region_creation(self):
        r = self.create_region()
        self.assertTrue(isinstance,(r,Region))
        self.assertEqual(r.__unicode__(),r.name)


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
