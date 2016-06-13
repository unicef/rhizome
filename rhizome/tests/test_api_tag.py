from base_test_case import RhizomeApiTestCase
from django.contrib.auth.models import User
from rhizome.models import Indicator, IndicatorToTag, IndicatorTag, LocationPermission, Location,\
    LocationType, Office


class IndicatorTagResourceTest(RhizomeApiTestCase):

    def setUp(self):
        super(IndicatorTagResourceTest, self).setUp()

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

    def test_create_tag(self):
        post_data = {"tag_name": "test tag name", 'id': -1}

        IndicatorTag.objects.all().delete()
        self.assertEqual(IndicatorTag.objects.count(), 0)

        resp = self.api_client.post('/api/v1/indicator_tag/', format='json',
                                    data=post_data, authentication=self.get_credentials())
        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertNotEqual(post_data['id'], response_data['id'])
        self.assertEqual(IndicatorTag.objects.count(), 1)
        self.assertNotEqual(IndicatorTag.objects.all()[0].id, -1)

    def test_update_tag(self):

        IndicatorTag.objects.all().delete()

        tag = IndicatorTag.objects.create(id=None,
                                          tag_name='Test Tag Name', )

        self.assertEqual(IndicatorTag.objects.count(), 1)
        new_tag_name = "New Tag Name"
        post_data = {"id": tag.id, "tag_name": new_tag_name}
        resp = self.api_client.post('/api/v1/indicator_tag/', format='json',
                                    data=post_data, authentication=self.get_credentials())

        response_data = self.deserialize(resp)

        self.assertHttpCreated(resp)
        self.assertEqual(tag.id, response_data['id'])
        self.assertEqual(IndicatorTag.objects.count(), 1)
        self.assertEqual(new_tag_name, response_data['tag_name'])

    def test_remove_tag(self):
        indicatior = Indicator.objects.create(short_name='Test Indicator',
                                              name='Test Indicator for the Tag',
                                              data_format='int',
                                              description='Test Indicator for the Tag Description', )

        tag = IndicatorTag.objects.create(tag_name='Test tag')

        IndicatorToTag.objects.all().delete()

        indicatior_tag = IndicatorToTag.objects.create(
            indicator_id=indicatior.id, indicator_tag_id=tag.id)

        self.assertEqual(IndicatorToTag.objects.count(), 1)

        delete_url = '/api/v1/indicator_to_tag/%s/' % str(indicatior_tag.id)

        self.api_client.delete(delete_url, format='json',
                               data={}, authentication=self.get_credentials())

        self.assertEqual(IndicatorToTag.objects.count(), 0)
