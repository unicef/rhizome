from django.test import TestCase
from django.contrib.auth.models import User

from source_data.models import Source, Document

class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):


        self.source = Source.objects.create(
            source_name = 'test',
            source_description = 'test')

        self.user = User.objects.create(username='test_user')

        self.document = Document.objects.create(
            doc_text = 'test_text',
            created_by_id  = self.user.id,
            guid = 'refresh_master_test')


    def test_refresh_master(self):

        self.set_up()

        self.assertEqual(1,1)
