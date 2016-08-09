from rhizome.tests.base_test_case import RhizomeApiTestCase
from django.contrib.auth.models import User
from rhizome.models.document_models import Document, SourceObjectMap, \
    DocumentSourceObjectMap, SourceSubmission
from pandas import read_csv, notnull, to_datetime

from rhizome.models.office_models import Office
from rhizome.models.campaign_models import Campaign
from rhizome.models.location_models import Location, LocationType
from rhizome.models.indicator_models import Indicator, IndicatorTag


class TestSetupHelpers(RhizomeApiTestCase):

    def __init__(self):
        self.username = "test_user"
        self.password = "test_password"
        self.user = User.objects\
            .create_user(self.username, 'test@test.com', self.password)

    def get_credentials(self, test_class):
        result = test_class.api_client.client.login(
            username=self.username, password=self.password)
        return result

    def create_arbitrary_office(self, name='Earth'):
        return Office.objects.create(name=name)

    def create_arbitrary_location_type(self):
        return LocationType.objects.create(name='test', admin_level=0)

    def create_arbitrary_location(self, location_type_id, office_id, location_name='Somalia', location_code='Somalia', parent_location_id=None):
        if parent_location_id:
            return Location.objects.create(
                name=location_name,
                location_code=location_code,
                location_type_id=location_type_id,
                office_id=office_id,
                parent_location_id=parent_location_id
            )
        else:
            return Location.objects.create(
                name=location_name,
                location_code=location_code,
                location_type_id=location_type_id,
                office_id=office_id
            )

    def create_arbitrary_som(self, source_object_code='Percent missed children_PCA', id=None, content_type='indicator'):
        if id:
            return SourceObjectMap.objects.create(
                source_object_code=source_object_code,
                content_type='indicator',
                mapped_by_id=self.user.id,
                master_object_id=id,
            )
        else:
            return SourceObjectMap.objects.create(
                source_object_code=source_object_code,
                content_type='indicator',
                mapped_by_id=self.user.id,
                master_object_id=-1
            )

    def create_arbitrary_document(self, document_docfile='eoc_post_campaign.csv', doc_title='eoc_post_campaign.csv', id=None, file_type=None):
        document = ""
        if id:
            document = Document.objects.create(
                doc_title=doc_title,
                file_type=file_type,
                created_by_id=self.user.id,
                guid='test',
                id=id)
        else:
            document = Document.objects.create(
                doc_title=doc_title,
                file_type=file_type,
                created_by_id=self.user.id,
                guid='test')
        document.docfile = document_docfile
        document.save()
        return document

    def create_arbitrary_dsom(self, document_id, som_id, id=None):
        if id:
            return DocumentSourceObjectMap.objects.create(
                document_id=document_id,
                source_object_map_id=som_id,
                id=23)
        else:
            return DocumentSourceObjectMap.objects.create(
                document_id=document_id,
                source_object_map_id=som_id)

    def post(self, test_class, uri, data=None):
        if data:
            return test_class.api_client\
                .post(uri,format='json', data=data, \
                authentication=self.get_credentials(test_class))
        else:
            return test_class.api_client\
                .post(uri,format='json',\
                authentication=self.get_credentials(test_class))

    def get(self, test_class, uri, data=None):
        if data:
            return test_class.api_client.get(uri, format='json', data=data,\
                authentication=self.get_credentials(test_class))
        else:
            return test_class.api_client.get(uri,format='json',\
                authentication=self.get_credentials(test_class))

    def delete(self, test_class, uri, data=None):
        if data:
            return stest_class.api_client.delete(uri, format='json', data=data,\
                 authentication=self.get_credentials(test_class))
        else:
            return test_class.api_client.delete(uri, format='json',\
                authentication=self.get_credentials(test_class))

    def patch(self, test_class, uri, data=None):
        if data:
            return test_class.api_client\
                .patch(uri,format='json', data=data, \
                authentication=self.get_credentials(test_class))
        else:
            return test_class.api_client\
                .patch(uri,format='json',\
                authentication=self.get_credentials(test_class))

    def model_df_to_data(self, model_df, model):
        meta_ids = []
        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()
        for row_ix, row_dict in list_of_dicts.iteritems():
            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)
        return meta_ids

    def create_arbitrary_campaign(self, office_id, campaign_type_id, \
        location_id, indicator_tag_id, name="test"):
        return Campaign.objects.create(
            start_date='2016-01-01',
            end_date='2016-01-01',
            office_id=office_id,
            campaign_type_id=campaign_type_id,
            name=name
        )

    def create_arbitrary_indicator(self, name='test', short_name="test2"):
        return Indicator.objects\
            .create(short_name=short_name,
                    name=name,
                    description='Test Indicator for the Tag 2 Description')

    def ingest_file(self, file_name):
        document = Document.objects.create(
            doc_title=file_name,
            created_by_id=self.user.id,
            guid='test')
        document.docfile = file_name
        document.save()
        document.transform_upload()

        return document.id

    def create_arbitrary_ss(self, doc_id, data_date='2016-01-01'):
        return SourceSubmission.objects.create(
            document_id=doc_id,
            submission_json='',
            row_number=0,
            data_date=data_date)

    # pre loads a top level indicator tag, locations, campaigns, indicators
    def load_some_metadata(self):
        top_lvl_tag = IndicatorTag.objects.create(id=1, tag_name='Polio')
        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])

        location_df = read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        office_id = Office.objects.create(id=1, name='test').id

        self.locations = self.model_df_to_data(location_df, Location)
        self.campaigns = self.model_df_to_data(campaign_df, Campaign)
        self.indicators = self.model_df_to_data(indicator_df, Indicator)
