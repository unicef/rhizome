from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from pandas import read_csv, notnull, to_datetime

from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform
from rhizome.models import *
from django.core.exceptions import ObjectDoesNotExist

class TransformUploadTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(TransformUploadTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        self.create_metadata()
        self.user = User.objects.get(username = 'test')
        self.location_list = Location.objects.all().values_list('name',flat=True)

    def test_simple_transform(self):

        self.ingest_file('eoc_post_campaign.csv')

        the_value_from_the_database = DataPointComputed.objects.get(
                campaign_id = self.mapped_campaign_id,
                indicator_id = self.mapped_indicator_with_data,
                location_id = self.mapped_location_id
            ).value

        some_cell_value_from_the_file = 0.082670906
        ## find this from the data frame by selecting the cell where we have mapped the data..

        self.assertEqual(some_cell_value_from_the_file, the_value_from_the_database)

    def test_upload_new_data(self):

        file_and_cell_vals ={'eoc_post_campaign.csv': 0.082670906, 'modified_single_cell.csv': 0.0324}

        for file, cell_val_from_file in file_and_cell_vals.iteritems():
            self.ingest_file(file)

            the_value_from_the_database = DataPointComputed.objects.get(
                    campaign_id = self.mapped_campaign_id,
                    indicator_id = self.mapped_indicator_with_data,
                    location_id = self.mapped_location_id
                ).value

            #test that the file cell value reflects that in the database
            self.assertEqual(cell_val_from_file, the_value_from_the_database)

    def test_upsert_source_object_map(self):
        source_map_entry = SourceObjectMap.objects.filter(
            source_object_code = 'AF001039006000000000',
            content_type = 'location'
            )
        self.assertEqual(0, len(source_map_entry))

        document_id = self.ingest_file('eoc_post_campaign.csv')

        source_map_entry = SourceObjectMap.objects.filter(
            source_object_code = 'AF001039006000000000',
            content_type = 'location'
            )
        self.assertEqual(1, len(source_map_entry))

        #makes sure that we update DSOM as well
        dsom_entry = DocumentSourceObjectMap.objects.filter(
            document_id=document_id,
            source_object_map_id=source_map_entry[0].id)
        self.assertEqual(1, len(dsom_entry))

    def test_simple_transform(self):

        self.ingest_file('eoc_post_campaign.csv')

        the_value_from_the_database = DataPointComputed.objects.get(
                campaign_id = self.mapped_campaign_id,
                indicator_id = self.mapped_indicator_with_data,
                location_id = self.mapped_location_id
            ).value

        some_cell_value_from_the_file = 0.082670906
        ## find this from the data frame by selecting the cell where we have mapped the data..

        self.assertEqual(some_cell_value_from_the_file, the_value_from_the_database)

    def test_dupe_metadata_mapping(self):

        #duplicate of master_object_id that's used in create_metadata
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed due to not visited',
            content_type = 'indicator',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_indicator_with_data
        )

        self.ingest_file('eoc_post_campaign.csv')

        #the indicator should have not been added
        try:
            the_value_from_the_database = DataPointComputed.objects.get(
                campaign_id = self.mapped_campaign_id,
                indicator_id = self.mapped_indicator_with_data,
                location_id = self.mapped_location_id
            )
            fail("the value should not have been added due to duplicated indicator id")
        except ObjectDoesNotExist:
            pass


    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        top_lvl_tag = IndicatorTag.objects.create(id = 1, tag_name='Polio')

        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['top_lvl_indicator_tag_id'] = top_lvl_tag.id

        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])

        location_df= read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        print indicator_df

        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2, \
            date_attempted = '2015-01-01',is_error = False)

        campaign_type = CampaignType.objects.create(id=1,name="test")

        locations = self.model_df_to_data(location_df,Location)
        campaigns = self.model_df_to_data(campaign_df,Campaign)
        indicators = self.model_df_to_data(indicator_df,Indicator)
        self.user_id = User.objects.create_user('test','test@test.com', 'test').id
        self.mapped_location_id = locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code = 'AF001039003000000000',
            content_type = 'location',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code = source_campaign_string,
            content_type = 'campaign',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_campaign_id
        )
        self.mapped_indicator_id_0 = locations[0].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed children_PCA',
            content_type = 'indicator',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_indicator_id_0
        )


        self.mapped_indicator_with_data = locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed due to other reasons',
            content_type = 'indicator',
            mapped_by_id = self.user_id,
            master_object_id = self.mapped_indicator_with_data
        )


    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids

    def ingest_file(self, file_name):
        ## create one doc ##
        document = Document.objects.create(
        doc_title = file_name,
        created_by_id = self.user_id,
        guid = 'test')
        document.docfile = file_name
        document.save()
        sdt = SimpleDocTransform(self.user.id, document.id)
        sdt.main()
        return document.id
