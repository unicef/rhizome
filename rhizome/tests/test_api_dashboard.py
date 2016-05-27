from base_test_case import RhizomeAPITestCase
from django.contrib.auth.models import User
from rhizome.models import CustomDashboard, CustomChart, LocationPermission,\
    Location, LocationType, Office

import json


class DashboardResourceTest(RhizomeAPITestCase):

    def setUp(self):
        super(DashboardResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
                                             'john@john.com', self.password)

        self.lt = LocationType.objects.create(name='test', admin_level=0)
        self.o = Office.objects.create(name='Earth')

        self.top_lvl_location = Location.objects.create(
            name='Nigeria',
            location_code='Nigeria',
            location_type_id=self.lt.id,
            office_id=self.o.id,
        )

        LocationPermission.objects.create(user_id=self.user.id,
                                          top_lvl_location_id=self.top_lvl_location.id)

        self.get_credentials()

        # create their api_key

    def get_credentials(self):
        result = self.api_client.client.login(username=self.username,
                                              password=self.password)
        return result

    def test_dashboard_post(self):
        post_data = {'title': 'the dashboard title'}
        CustomDashboard.objects.all().delete()
        self.assertEqual(CustomDashboard.objects.count(), 0)

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',
                                    data=post_data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)
        self.assertHttpCreated(resp)
        self.assertEqual(post_data['title'], response_data['title'])
        self.assertEqual(CustomDashboard.objects.count(), 1)

    def test_dashboard_post_rows(self):
        dboard_title = 'the dashboard title'
        dboard_rows = json.dumps([{'charts': ['fdfdf'], 'layout':1}, {
                                 'charts': ['ddsds'], 'layout':2}])
        post_data = {
            'title': dboard_title,
            'rows': dboard_rows
        }
        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',
                                    data=post_data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.deserialize(resp)
        self.assertEqual(CustomDashboard.objects.count(), 1)
        dboard = CustomDashboard.objects.get(title=dboard_title)
        self.assertEqual(json.dumps(dboard.rows), dboard_rows)

    def test_dashboard_post_no_params(self):
        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',
                                    data={}, authentication=self.get_credentials())
        self.assertHttpApplicationError(resp)

    def test_dashboard_chart_post(self):

        ## create two charts ##
        c1 = CustomChart.objects.create(uuid='a', title='a', chart_json='')
        c2 = CustomChart.objects.create(uuid='b', title='b', chart_json='')

        dashboard_title = '2 Chart Dashboard'
        chart_uuids = '%s,%s' % (c1.uuid, c2.uuid)
        post_data = {
            'title': dashboard_title,
            'chart_uuids': chart_uuids
        }

        ## post the dashboard title and the associated charts to the API ##
        resp = self.api_client.post('/api/v1/custom_dashboard/',
                                    format='json',
                                    data=post_data,
                                    authentication=self.get_credentials()
                                    )

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(response_data['title'], dashboard_title)
        self.assertEqual(response_data['chart_uuids'].split(
            ','), [c1.uuid, c2.uuid])

    def test_dashboard_name_exist(self):
        dashboard_name = "test the already exists"

        CustomDashboard.objects.all().delete()
        self.assertEqual(CustomDashboard.objects.count(), 0)

        post_data = {'title': dashboard_name}
        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',
                                    data=post_data, authentication=self.get_credentials())
        self.assertEqual(CustomDashboard.objects.count(), 1)

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json',
                                    data=post_data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)

        self.assertHttpApplicationError(resp)
        self.assertEqual(CustomDashboard.objects.count(), 1)
        self.assertEqual('the custom dashboard "{0}" already exists'.format(
            dashboard_name), response_data['error'])

    def test_dashboard_get_no_params(self):
        d1 = CustomDashboard.objects.create(title="1 d-board")
        d2 = CustomDashboard.objects.create(title="2 d-board")
        resp = self.api_client.get('/api/v1/custom_dashboard/',
                                   format='json',
                                   authentication=self.get_credentials())

        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(len(resp_data['objects']), 2)

    def test_dashboard_get_rows(self):
        ## create two charts ##
        c1 = CustomChart.objects.create(uuid='a', title='a', chart_json=json.dumps({
                                        'foo': 'bar', 'title': 'sometitle'}))
        c2 = CustomChart.objects.create(uuid='b', title='b', chart_json=json.dumps({
                                        'foo1': 'bar1', 'title1': 'sometitle1'}))
        c3 = CustomChart.objects.create(uuid='c', title='c', chart_json=json.dumps({
                                        'c1': 'c2', 'title2': 'sometitle2'}))
        dboard_rows = [{'charts': [c1.uuid], 'layout':1},
                       {'charts': [c2.uuid, c3.uuid], 'layout':2}]
        d = CustomDashboard.objects.create(title="1 d-board", rows=dboard_rows)

        resp = self.api_client.get('/api/v1/custom_dashboard/%s/' % d.id,
                                   format='json',
                                   authentication=self.get_credentials())

        response_data = self.deserialize(resp)
        # print response_data
        self.assertValidJSONResponse(resp)
        self.assertEqual(len(response_data['rows']), len(dboard_rows))
        # make sure all the right charts are added in the right places
        for idx, row in enumerate(response_data['rows']):
            for idx2, chart in enumerate(row['charts']):
                self.assertEqual(chart['uuid'], dboard_rows[
                                 idx]['charts'][idx2])

    def test_dashboard_get(self):
        ## create a dashboard ##
        dashboard_title = 'Another one of these Dashboards'
        d = CustomDashboard.objects.create(title=dashboard_title)

        ## create two charts ##
        c1 = CustomChart.objects.create(uuid='1', title='bbbbb', chart_json=json.dumps({
                                        'foo1': 'bar1', 'title1': 'sometitle1'}))
        c2 = CustomChart.objects.create(uuid='2', title='aaaa', chart_json=json.dumps({
                                        'foo2': 'bar2', 'title2': 'sometitle2'}))

        get_data = {
            'id': d.id
        }
        resp = self.api_client.get('/api/v1/custom_dashboard/',
                                   format='json',
                                   data=get_data,
                                   authentication=self.get_credentials()
                                   )
        self.assertHttpOK(resp)
        resp_data = self.deserialize(resp)
        self.assertEqual(resp_data['objects'][0]['title'], dashboard_title)

    def test_delete_dashboard_detail(self):
        dashboard_name = "test delete a dashboard"

        # Create the custom dashboard
        CustomDashboard.objects.all().delete()
        self.assertEqual(CustomDashboard.objects.count(), 0)

        dashboard = CustomDashboard.objects.create(
            title=dashboard_name, layout=1)
        self.assertEqual(CustomDashboard.objects.count(), 1)

        delete_url = '/api/v1/custom_dashboard/%s/' % str(dashboard.id)

        resp = self.api_client.delete(
            delete_url, format='json', data={}, authentication=self.get_credentials())

        self.assertEqual(CustomDashboard.objects.count(), 0)

    # TODO: test for duplicate dashboard

    def test_delete_dashboard(self):
        dashboard_name = 'some d-board!'
        dashboard = CustomDashboard.objects.create(
            title=dashboard_name, layout=1)
        self.assertEqual(CustomDashboard.objects.count(), 1)

        delete_url = '/api/v1/custom_dashboard/?id=' + str(dashboard.id)

        resp = self.api_client.delete(
            delete_url, format='json', data={}, authentication=self.get_credentials())
        self.assertEqual(CustomDashboard.objects.count(), 0)
