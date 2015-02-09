
from django.test import TestCase

class DataPointApiTestCase(TestCase):

    def set_up(self):

        pass


    def test_the_api(self):

        self.set_up()

    # def test_main_api(self):

    #     set_up_dict = self.set_up()
    #     dpi = Indicator.objects.create(
    #         name = 'test',
    #         description = 'test',
    #         is_reported = 0,
    #         source_id = set_up_dict['source_id']
    #     )

    #     self.assertTrue(isinstance,(dpi,Indicator))
    #     self.assertEqual(dpi.__unicode__(),dpi.name)
