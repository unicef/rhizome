import json

from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from setup_helpers import TestSetupHelpers
from pandas import read_csv, notnull, to_datetime
from rhizome.models import *

class ChartTypeResourceTest(ResourceTestCase):
    def setUp(self):
        super(ChartTypeResourceTest, self).setUp()

        self.ts = TestSetupHelpers()
        self.lt = self.ts.create_arbitrary_location_type()
        self.o = self.ts.create_arbitrary_office()

        self.top_lvl_location = self.ts.create_arbitrary_location(self.lt.id, self.o.id)

        LocationPermission.objects.create(user_id = self.ts.user.id,\
            top_lvl_location_id = self.top_lvl_location.id)

    #GET request, returns all the chart types.
    def test_get_chart_type(self):
    	resp = self.ts.get(self, '/api/v1/chart_type/')
    	self.assertHttpOK(resp)



