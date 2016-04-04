from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from pandas import read_csv, notnull, to_datetime

from rhizome.etl_tasks.transform_upload import ComplexDocTransform
from rhizome.models import *
from rhizome.etl_tasks.refresh_master import MasterRefresh


class TransformUploadTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        super(TransformUploadTestCase, self).__init__(*args, **kwargs)

    def setUp(self):
        self.create_metadata()
        self.user = User.objects.get(username = 'test')
        self.document = Document.objects.get(doc_title = 'test')
        self.test_file_location = 'ebola_data.csv'
        self.document.docfile = self.test_file_location
        self.document.save()


        self.location_list = Location.objects.all().values_list('name',flat=True)

    def test_doc_to_source_submission(self):
        '''
        Part of the set up method, this takes a csv and inserts it into the
        source submission table.  This method in context of this test represents
        what would happen when a user uploads a csv and the data flows through
        "etl_tasks/transform_upload"

        Uploading the csv to the server is itself a different task.. so for now
        we preform "transform_upload" on the test file.

        This method is in charge of one specific thing.. taking an input stream
        such as a csv, or an ODK submission, and creating one row in the
        database with the schema that it was received.  Later in the ingest
        process, users are allowed to specify settings to each file in order
        to translate them into data the application can consume and visualize.

        The Doc Transofrm Method is responsible for the following:
            1. Inserting one record into source_submission for each csv row
            2. Inserting any new mappings into source_object_map
            3. Associating *all* source_object_maps with self.document_id ( even
              those created in other documents)
            4. Inserting one record into submission_detail        '''

        dt = ComplexDocTransform(self.user.id, self.document.id)

        source_submissions = dt.process_file()

        test_file = open(settings.MEDIA_ROOT + self.test_file_location ,'r')
        file_line_count = sum(1 for line in test_file) - 1 # for the header!

        self.assertEqual(len(source_submissions),file_line_count)

    def test_missing_required_column(self):
        doc_id = self.ingest_file('missing_campaign.csv')
        try:
            ComplexDocTransform(self.user.id, doc_id)
            fail('should raise an exception')
        except Exception as err:
            self.assertEqual('campaign is a required column.', err.message)
            pass

    def test_duplicate_rows(self):
        doc_id = self.ingest_file('dupe_datapoints.csv')
        dt = ComplexDocTransform(self.user.id, doc_id)
        source_submissions = dt.main()
        mr = MasterRefresh(self.user.id, doc_id)
        mr.main()
        dps = DataPoint.objects.all()
        self.assertEqual(len(dps), 1)
        some_cell_value_from_the_file = 0.9029
        self.assertEqual(dps[0].value, some_cell_value_from_the_file)

    # test bad percent values for upload. for instance if a user uploads "95%" instead of '.95'
    #and make sure that the value has been correctly converted
    def test_percent_vals(self):
        doc_id = self.ingest_file('percent_vals.csv')
        ComplexDocTransform(self.user.id, doc_id).main()
        MasterRefresh(self.user.id, doc_id).main()
        dps = DataPoint.objects.all()
        self.assertEqual(len(dps), 2)
        expected_dp_val = 0.8267
        dp = DataPoint.objects.get(indicator_id = self.mapped_indicator_with_data)
        self.assertEqual(expected_dp_val, dp.value)

    

        #also add test to make sure that the value is correct

    # def test_boolean_transform(self):

    #     location_code_column = 'SettlementCode'
    #     campaign_code_colum = 'DateOfReport'
    #
    #     input_df = read_csv('/Users/john/Downloads/vcm_birth_tracking_results.csv')
    #     # input_df = read_csv('/Users/john/Desktop/vcm_bitrth_tracking_sample.csv')
    #
    #     cleaned_df = input_df\
    #         [[location_code_column,campaign_code_colum,'VCM0Dose','VCMNameCAttended']]
    #
    #     bool_map = {'yes': 1, 'no': 0}
    #
    #     cleaned_df['VCM0Dose'] = cleaned_df['VCM0Dose'].map(bool_map)
    #     cleaned_df['VCMNameCAttended'] = cleaned_df['VCMNameCAttended'].map(bool_map)
    #
    #     cleaned_df = cleaned_df.where((notnull(cleaned_df)), 0)
    #
    #     grouped_df = DataFrame(cleaned_df\
    #         .groupby([location_code_column,campaign_code_colum])[['VCMNameCAttended','VCM0Dose']].sum())
    #
    #     print grouped_df
    #
    #     row_count_df = DataFrame(cleaned_df\
    #         .groupby([location_code_column,campaign_code_colum])\
    #         .count())[[location_code_column]]
    #
    #     final_df = grouped_df.merge(row_count_df,left_index=True,right_index=True)
    #     final_df.rename(columns={location_code_column:'location_campaign_code_count'}, inplace=True)
    #
    #     return final_df


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
        calc_indicator_df = read_csv\
            ('rhizome/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','test@test.com', 'test').id
        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2, \
            date_attempted = '2015-01-01',is_error = False)

        document_id = Document.objects.create(
            doc_title = 'test',
            file_header = 'Campaign,Wardcode,uq_id,HHsampled,HHvisitedTEAMS,Marked0to59,UnImmun0to59,NOimmReas1,NOimmReas2,NOimmReas3,NOimmReas4,NOimmReas5,NOimmReas6,NOimmReas7,NOimmReas8,NOimmReas9,NOimmReas10,NOimmReas11,NOimmReas12,NOimmReas13,NOimmReas14,NOimmReas15,NOimmReas16,NOimmReas17,NOimmReas18,NOimmReas19,NOimmReas20,ZeroDose,TotalYoungest,YoungstRI,RAssessMrk,RCorctCAT,RIncorect,RXAssessMrk,RXCorctCAT,RXIncorect,STannounc,SRadio,STradlead,SReiliglead,SMosque,SNewspaper,SPoster,Sbanner,SRelative,SHworker,Scommmob,SNOTAWARE,Influence1,Influence2,Influence3,Influence4,Influence5,Influence6,Influence7,Influence8',
            created_by_id = user_id,
            guid = 'test').id

        for ddt in ['uq_id_column','username_column','image_col',
            'date_column','location_column','location_display_name']:

            DocDetailType.objects.create(name=ddt)

        for rt in ["country","settlement","province","district","sub-district"]:
            DocDetailType.objects.create(name=rt)


        campaign_type = CampaignType.objects.create(id=1,name="test")

        self.locations = self.model_df_to_data(location_df,Location)
        self.campaigns = self.model_df_to_data(campaign_df,Campaign)
        self.indicators = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)

        ## associate indicators with tag ##
        indicator_to_tag_ids = [IndicatorToTag(**{\
            'indicator_id':ind.id,\
            'indicator_tag_id': top_lvl_tag.id}) for ind in self.indicators]

        IndicatorToTag.objects.bulk_create(indicator_to_tag_ids)


        ## create the uq_id_column configuration ##

        uq_id_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='uq_id_column').id,
            doc_detail_value = 'uq_id'
        )

        location_column_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='location_column').id,
            doc_detail_value = 'Wardcode'
        )

        date_column_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='date_column').id,
            doc_detail_value = 'submission_date'
        )

        self.mapped_location_id = self.locations[0].id
        loc_map = SourceObjectMap.objects.create(
            source_object_code = 'AF001039003000000000',
            content_type = 'location',
            mapped_by_id = user_id,
            master_object_id = self.mapped_location_id
        )

        source_campaign_string = '2016 March NID OPV'
        self.mapped_campaign_id = self.campaigns[0].id
        campaign_map = SourceObjectMap.objects.create(
            source_object_code = source_campaign_string,
            content_type = 'campaign',
            mapped_by_id = user_id,
            master_object_id = self.mapped_campaign_id
        )
        self.mapped_indicator_id_0 = self.locations[0].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed children_PCA',
            content_type = 'indicator',
            mapped_by_id = user_id,
            master_object_id = self.mapped_indicator_id_0
        )


        self.mapped_indicator_with_data = self.locations[2].id
        indicator_map = SourceObjectMap.objects.create(
            source_object_code = 'Percent missed due to other reasons',
            content_type = 'indicator',
            mapped_by_id = user_id,
            master_object_id = self.mapped_indicator_with_data
        )
    def ingest_file(self, file_name):
        ## create one doc ##
        document = Document.objects.create(
        doc_title = file_name,
        created_by_id = self.user.id,
        guid = 'test')
        document.docfile = file_name
        document.save()
        return document.id

    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
