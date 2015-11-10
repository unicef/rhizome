from tastypie.test import ResourceTestCase
from django.contrib.auth.models import User
from datapoints.models import CustomDashboard

class DashboardResourceTest(ResourceTestCase):
    def setUp(self):
        super(DashboardResourceTest, self).setUp()

        # Create a user.
        self.username = 'john'
        self.password = 'pass'
        self.user = User.objects.create_user(self.username,
                                             'john@john.com', self.password)

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

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json', \
                                    data=post_data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(post_data['title'], response_data['title'])
        self.assertEqual(CustomDashboard.objects.count(), 1)

    def test_dashboard_name_exist(self):
        dashboard_name = "test the already exists"

        CustomDashboard.objects.all().delete()
        self.assertEqual(CustomDashboard.objects.count(), 0)

        post_data = {'title': dashboard_name}
        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json', \
                                    data=post_data, authentication=self.get_credentials())
        self.assertEqual(CustomDashboard.objects.count(), 1)

        resp = self.api_client.post('/api/v1/custom_dashboard/', format='json', \
                                    data=post_data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)

        self.assertHttpApplicationError(resp)
        self.assertEqual(CustomDashboard.objects.count(), 1)
        self.assertEqual('the custom dashboard "{0}" already exists'.format(dashboard_name), response_data['error'])
