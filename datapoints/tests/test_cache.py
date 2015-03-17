
from django.test import TestCase


class CacheRefreshTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(CacheRefreshTestCase, self).__init__(*args, **kwargs)

    def set_up(self):

        print 'TESTING\n' * 10

        # self.source = Source.objects.create(
        #     source_name = 'test',
        #     source_description = 'test')
        #
        # self.user = User.objects.create(
        #     username='john')
        #
        # self.document = Document.objects.create(
        #     doc_text = 'test',
        #     created_by_id = self.user.id,
        #     guid = 'test')

    def test_basic(self):

        self.set_up()

        self.assertEqual(1,1)
