import json

from django.test import TestCase
from django.contrib.auth.models import User
from pandas import read_csv, notnull, to_datetime

from rhizome.etl_tasks.transform_upload import ComplexDocTransform
from rhizome.etl_tasks.refresh_master import MasterRefresh
from rhizome.models import *


class RefreshMasterTestCase(TestCase):

    def __init__(self, *args, **kwargs):

        self.location_code_input_column = 'geocode'
        self.campaign_code_input_column = 'campaign'
        self.data_date_input_column = 'submission_date'
        self.uq_code_input_column = 'uq_id'

        super(RefreshMasterTestCase, self).__init__(*args, **kwargs)

    def set_up(self):
        '''
        Refresh master needs a few peices of metadata to be abel to do it's job.
        Location, Campaign, User .. all of the main models that you can see
        initialized in the first migrations in the datapoints application.

        The set up method also runs the ComplexDocTransform method which simulates
        the upload of a csv or processing of an ODK submission.  Ideally this
        test will run independently of this module, but for now this is how
        we initialize data in the system via the .csv below.
        '''
        self.test_file_location = 'ebola_data.csv'
        self.location_list = Location.objects.all().values_list('name',flat=True)
        self.create_metadata()
        self.user = User.objects.get(username = 'test')

        self.document = Document.objects.get(doc_title = 'test')
        self.document.docfile = self.test_file_location
        self.document.save()

        dt = ComplexDocTransform(self.user.id, self.document.id)
        dt.main()

    def test_refresh_master_init(self):

        self.set_up()
        mr = MasterRefresh(self.user.id ,self.document.id)

        self.assertTrue(isinstance,(mr,MasterRefresh))

    def test_submission_detail_refresh(self,):

        self.set_up()
        mr = MasterRefresh(self.user.id ,self.document.id)

        source_submissions_data = SourceSubmission.objects\
            .filter(document_id = self.document.id)\
            .values_list('id',flat=True)

        mr.refresh_submission_details()
        submission_details = SourceSubmission.objects\
            .filter(document_id = self.document.id)

        self.assertEqual(len(source_submissions_data)\
            ,len(submission_details))

    # def test_data_that_needs_campaign(self):
    #     '''
    #     AFter syncing a document, the system needs to ensure that data that
    #     has no associated campaign, will be marked with a cache_job_id of -2.
    #
    #     The aggregation framework searches for datapitns with cache_job_id = -1
    #     but if one of these datapoitns has no associated campaign, then
    #     aggregation will break.
    #
    #     Thus we must ensure that any data that needs campaign is marked
    #     accordingly, so we dont break aggregation, and so the user knows that
    #     there is data in the recent upload that needs to have an associated
    #     campaign.
    #
    #     python manage.py test rhizome.tests.test_refresh_master\
    #     .RefreshMasterTestCase.test_data_that_needs_campaign \
    #     --settings=rhizome.settings.test
    #     '''
    #
    #     self.set_up()
    #
    #
    #     office_obj = Office.objects.all()[0]
    #     tag_obj = IndicatorTag.objects.all()[0]
    #     location_obj = Location.objects.all()[0]
    #     indicator_obj = Indicator.objects.all()[0]
    #     campaign_type_obj = CampaignType.objects.all()[0]
    #     start_date, end_date, bad_date = '2016-12-01','2016-12-30','2017-01-01'
    #     source_submission_obj = SourceSubmission.objects.all()[0]
    #
    #     my_campaign = Campaign.objects.create(
    #         start_date = start_date,
    #         end_date = end_date,
    #         name = 'my_campaign',
    #         top_lvl_location = location_obj,
    #         top_lvl_indicator_tag = tag_obj,
    #         office = office_obj,
    #         campaign_type = campaign_type_obj
    #     )
    #
    #     ## skipping over all of the refresH-master methos
    #     ## and  just testing this particular test case
    #     base_dp_dict = {
    #         'location_id': location_obj.id,
    #         'indicator_id': indicator_obj.id,
    #         'value': 100,
    #         'source_submission_id': source_submission_obj.id,
    #     }
    #
    #     ## create dictionaries for the two datapoints ##
    #     no_campaign_dp_dict = {'data_date' : bad_date}
    #     has_campaign_dp_dict = {'data_date' : start_date}
    #
    #     no_campaign_dp_dict.update(base_dp_dict)
    #     has_campaign_dp_dict.update(base_dp_dict)
    #
    #     ## create the datapoints ##
    #     dp_without_campaign = DataPoint.objects.create(**no_campaign_dp_dict)
    #     dp_with_campaign = DataPoint.objects.create(**has_campaign_dp_dict)
    #
    #     ## instantiate the MasterRefresh object ##
    #     mr = MasterRefresh(self.user.id, self.document.id)
    #     mr.ss_ids_to_process = [source_submission_obj]
    #
    #     ## this is the method we are testing ##
    #     mr.mark_datapoints_with_needs_campaign()
    #
    #     ## now fetch the data after updating the cache_job_ids ##
    #     no_campaign_dp_dict.pop('cache_job_id', None)
    #     no_campaign = DataPoint.objects.get(**no_campaign_dp_dict)
    #     has_campaign = DataPoint.objects.get(**has_campaign_dp_dict)
    #
    #     self.assertEqual(has_campaign.cache_job_id,-1)
    #     self.assertEqual(no_campaign.cache_job_id,-2)

    def test_latest_data_gets_synced(self):
        '''
        I upload a spreadsheet on tuesday, but i realized that the data was wrong, so i upload another sheet with the same locations, dates
        and indicators.  The new spreasheet should override, and not aggregate any duplicative data.
        '''

        self.set_up()


        test_ind_id = Indicator.objects.all()[0].id
        test_loc_id = Location.objects.all()[0].id
        test_campaign_id = Campaign.objects.all()[0].id

        bad_val, good_val = 10, 20
        data_date = '2015-12-31'
        ss_old = SourceSubmission.objects\
            .filter(document_id = self.document.id)[0]


        doc_to_override = Document.objects.create(
                doc_title = 'override',
                created_by_id = self.user.id,
                guid = 'override'
        )

        ss_new = SourceSubmission.objects.create(
            document_id = doc_to_override.id,
            instance_guid = 'override',
            row_number = 1,
            data_date = '2016-01-01',
            location_code = 'OVERRIDE',
            location_display = 'OVERRIDE',
            submission_json = '',
            process_status = 1
        )

        base_doc_dp_dict = {
            'document_id' : self.document.id,
            'indicator_id' : test_ind_id,
            'location_id' : test_loc_id,
            'campaign_id': test_campaign_id,
            'data_date' : data_date,
            'agg_on_location': True,
        }

        bad_doc_dp_dict = {
            'value' : bad_val,
            'data_date' : data_date,
            'campaign_id': test_campaign_id,
            'source_submission_id' : ss_old.id,
        }
        bad_doc_dp_dict.update(base_doc_dp_dict)

        good_doc_dp_dict = {
            'value' : good_val,
            'data_date' : data_date,
            'campaign_id': test_campaign_id,
            'source_submission_id' : ss_new.id,
        }
        good_doc_dp_dict.update(base_doc_dp_dict)

        DocDataPoint.objects.create(**good_doc_dp_dict)
        DocDataPoint.objects.create(**bad_doc_dp_dict)

        mr = MasterRefresh(self.user.id, self.document.id)

        mr.sync_datapoint([ss_old.id, ss_new.id])

        dp_result = DataPoint.objects.filter(
            location_id = test_loc_id,
            indicator_id = test_ind_id,
            data_date = data_date
        )

        self.assertEqual(1,len(dp_result))
        self.assertEqual(good_val, dp_result[0].value)

    def test_submission_to_datapoint(self):
        '''
        This simulates the following use case:

        As a user journey we can describe this test case as:
            - user uploads file ( see how set_up method calls ComplexDocTransform )
            - user maps metadata
            - user clicks " refresh master "
                -> user checks to see if data is correct
            - user realizes that the data is wrong, due to an invalid mapping
            - user re-mapps the data and clicks " refresh master"
                -> data from old mapping should be deleted and associated to
                   the newly mapped value

        TEST CASES:
            1. WHen the submission detail is refreshed, the location/campaign ids
               that we mapped should exist in that row.
            2. DocDataPoint records are created if the necessary mapping exists
            3. There are no zero or null values allowed in doc_datapoint
            4. The doc_datapoint from #3 is merged into datpaoint.
            5. I create mappings, sync data, realize the mapping was incorrect,
               re-map the metadata and the old data should be deleted, the new
               data created.
                 -> was the old data deleted?
                 -> was the new data created?
        '''

        self.set_up()

        submission_qs = SourceSubmission.objects\
            .filter(document_id = self.document.id)\
            .values_list('id','submission_json')[0]

        ss_id, first_submission = submission_qs[0],json.loads(submission_qs[1])

        location_code = first_submission[self.location_code_input_column]
        campaign_code = first_submission[self.campaign_code_input_column]
        data_date = first_submission[self.data_date_input_column]
        raw_indicator_list = [k for k,v in first_submission.iteritems()]

        indicator_code = raw_indicator_list[-1]

        ## SIMULATED USER MAPPING ##
        ## see: source-data/Nigeria/2015/06/mapping/2

        ## choose meta data values for the source_map update ##
        map_location_id = Location.objects.all()[0].id
        first_indicator_id = Indicator.objects.all()[0].id
        first_campaign = Campaign.objects.all()[0].id

        ## map location ##
        som_id_l = SourceObjectMap.objects.get(
            content_type = 'location',
            source_object_code = location_code,
        )
        som_id_l.master_object_id = map_location_id
        som_id_l.save()

        ## map indicator ##
        som_id_i = SourceObjectMap.objects.get(
            content_type = 'indicator',
            source_object_code = indicator_code,
        )
        som_id_i.master_object_id = first_indicator_id
        som_id_i.save()

        ## map campaign ##
        som_id_c = SourceObjectMap.objects.get(
            content_type = 'campaign',
            source_object_code = campaign_code,
        )
        som_id_c.master_object_id = first_campaign
        som_id_c.save()

        mr_with_new_meta = MasterRefresh(self.user.id ,self.document.id)
        mr_with_new_meta.refresh_submission_details()

        first_submission_detail = SourceSubmission.objects\
            .get(id = ss_id)

        ## Test Case 2 ##
        self.assertEqual(first_submission_detail.get_location_id(), map_location_id)

        ## now that we have created the mappign, "refresh_master" ##
        ##         should create the relevant datapoints          ##

        mr_with_new_meta.submissions_to_doc_datapoints()
        doc_dp_ids = DocDataPoint.objects.filter(document_id =
            self.document.id,indicator_id=first_indicator_id).values()

        ## Test Case #3
        self.assertEqual(1,len(doc_dp_ids))

        mr_with_new_meta.sync_datapoint()
        dps = DataPoint.objects.all()

        ## Test Case #4
        self.assertEqual(1,len(dps))

        ## Test Case #5

        ## update the mapping with a new indicator value ##
        new_indicator_id = Indicator.objects.all()[1].id
        som_id_i.master_object_id = new_indicator_id
        som_id_i.save()

        mr_after_new_mapping = MasterRefresh(self.user.id ,self.document.id)
        mr_after_new_mapping.main()

        dp_with_new_indicator = DataPoint.objects.filter(indicator_id = \
            new_indicator_id)

        dp_with_old_indicator = DataPoint.objects.filter(indicator_id = \
            first_indicator_id)

        ## did new indicator flow through the system ?##
        self.assertEqual(1,len(dp_with_new_indicator))

        ## did the old indicator data get deleted?
        self.assertEqual(0,len(dp_with_old_indicator))



    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        top_lvl_tag = IndicatorTag.objects.create(id = 1, tag_name='Polio')
        campaign_df = read_csv('rhizome/tests/_data/campaigns.csv')
        campaign_df['top_lvl_indicator_tag_id'] = top_lvl_tag.id

        location_df= read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')
        calc_indicator_df = read_csv\
            ('rhizome/tests/_data/calculated_indicator_component.csv')

        user_id = User.objects.create_user('test','john@john.com', 'test').id
        office_id = Office.objects.create(id=1,name='test').id

        cache_job_id = CacheJob.objects.create(id = -2,date_attempted = '2015-01-01',\
            is_error = False)

        document_id = Document.objects.create(
            doc_title = 'test',
            created_by_id = user_id,
            guid = 'test').id

        for ddt in ['uq_id_column','username_column','image_col',
            'date_column','location_column','location_display_name']:

            DocDetailType.objects.create(name=ddt)

        for rt in ["country","settlement","province","district","sub-district"]:
            DocDetailType.objects.create(name=rt)


        campaign_type = CampaignType.objects.create(id=1,name="test")

        location_ids = self.model_df_to_data(location_df,Location)

        campaign_df['start_date'] = to_datetime(campaign_df['start_date'])
        campaign_df['end_date'] = to_datetime(campaign_df['end_date'])
        campaign_ids = self.model_df_to_data(campaign_df,Campaign)

        indicator_ids = self.model_df_to_data(indicator_df,Indicator)
        calc_indicator_ids = self.model_df_to_data(calc_indicator_df,\
            CalculatedIndicatorComponent)

        rg_conif = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='location_column').id,
            doc_detail_value = self.location_code_input_column

        )

        cp_conif = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='date_column').id,
            doc_detail_value = self.data_date_input_column
        )

        uq_id_config = DocumentDetail.objects.create(
            document_id = document_id,
            doc_detail_type_id = DocDetailType\
                .objects.get(name='uq_id_column').id,
            doc_detail_value = self.uq_code_input_column
        )

    def test_campaign_data_ingest(self):
        # ./manage.py test rhizome.tests.test_refresh_master.RefreshMasterTestCase.test_campaign_data_ingest --settings=rhizome.settings.test

        self.set_up()
        test_file_location = 'allAccessData.csv'
        test_df = read_csv('rhizome/tests/_data/' + test_file_location)

        document = Document.objects.create(doc_title = 'allAccessData')
        document.docfile = test_file_location
        document.save()

        ## create locatino_meta ##
        distinct_location_codes = test_df['geocode'].unique()
        for l in distinct_location_codes:
            l_id = Location.objects.create(
                name = l,
                location_code = l,
                location_type_id = 1,
                office_id = 1
            ).id
            l_som = SourceObjectMap.objects.create(
                    master_object_id = l_id,
                    content_type = 'location',
                    source_object_code = str(l)
                )

        ## create campaign meta ##
        distinct_campaign_codes = test_df['campaign'].unique()
        for i, (c) in enumerate(distinct_campaign_codes):
            c_id = Campaign.objects.create(
                name = c,
                top_lvl_location_id = 1,
                top_lvl_indicator_tag_id = 1,
                office_id = 1,
                campaign_type_id =1,
                start_date = '2010-01-0' + str(i + 1),
                end_date  = '2010-01-0' + str(i + 1)
            ).id
            c_som = SourceObjectMap.objects.create(
                    master_object_id = c_id,
                    content_type = 'campaign',
                    source_object_code = str(c)
                )

        ## create indicator_meta ##
        access_indicator_id = Indicator.objects.create(
            name = 'access', short_name = 'access'
        ).id

        som_obj = SourceObjectMap.objects.create(
            master_object_id = access_indicator_id,
            content_type = 'indicator',
            source_object_code = '# Missed children due to inaccessibility (NEPI)'
        )

        dt = ComplexDocTransform(self.user.id, document.id)
        dt.main()

        mr = MasterRefresh(self.user.id, document.id)
        mr.main()

        ss_id_list = SourceSubmission.objects\
            .filter(document_id = document.id)\
            .values_list('id', flat=True)

        doc_dp_id_list = DocDataPoint.objects\
            .filter(source_submission_id__in = ss_id_list)\
            .values_list('id', flat=True)

        print 'doc_dp_id_list\n' * 10
        print doc_dp_id_list

        self.assertEqual(len(ss_id_list), len(test_df))

    def model_df_to_data(self,model_df,model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids
