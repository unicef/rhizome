from django.contrib.auth.models import User
from pandas import read_csv, notnull, DataFrame
from numpy import isnan
from django.test import TestCase

from rhizome.models import Office, CacheJob, LocationType, Campaign, Location,\
    CampaignType, Document, SourceSubmission, Indicator, IndicatorTag,\
    IndicatorToTag, CampaignToIndicator, CalculatedIndicatorComponent, \
    DataPoint, DataPointComputed, AggDataPoint, LocationTree
from rhizome.agg_tasks import AggRefresh
from rhizome.cache_meta import LocationTreeCache, OldLocationTreeCache
from setup_helpers import TestSetupHelpers


class AggRefreshTestCase(TestCase):

    '''
    from rhizome.agg_tasks import AggRefresh
    mr = AggRefresh()
    '''

    def __init__(self, *args, **kwargs):

        super(AggRefreshTestCase, self).__init__(*args, **kwargs)

    def setUp(self):

        self.ts = TestSetupHelpers()
        data_df = read_csv('rhizome/tests/_data/calc_data.csv')
        self.create_metadata()
        self.user = User.objects.get(username="test")

        self.test_df = data_df[data_df['is_raw'] == 1]
        self.target_df = data_df[data_df['is_raw'] == 0]
        self.campaign_id = Campaign.objects.all()[0].id
        self.top_lvl_location = Location.objects.filter(name='Nigeria')[0]
        # ltr = OldLocationTreeCache() ## LocationTreeCache()
        ltr = LocationTreeCache()
        ltr.main()

    def create_metadata(self):
        '''
        Creating the Indicator, location, Campaign, meta data needed for the
        system to aggregate / caclulate.
        '''

        read_csv('rhizome/tests/_data/campaigns.csv')
        location_df = read_csv('rhizome/tests/_data/locations.csv')
        indicator_df = read_csv('rhizome/tests/_data/indicators.csv')

        user_id = User.objects.create_user('test', 'john@john.com', 'test').id

        self.office_id = Office.objects.create(id=1, name='test').id

        cache_job_id = CacheJob.objects.create(
            id=-1, date_completed='2015-01-01', date_attempted='2015-01-01', is_error=False)

        self.location_type1 = LocationType.objects.create(admin_level=0,
                                                          name="country", id=1)
        self.location_type2 = LocationType.objects.create(admin_level=1,
                                                          name="province", id=2)

        campaign_type1 = CampaignType.objects.create(name='test')

        self.locations = self.model_df_to_data(location_df, Location)
        self.indicators = self.model_df_to_data(indicator_df, Indicator)
        ind_tag = IndicatorTag.objects.create(tag_name='Polio')
        sub_tag = IndicatorTag.objects.create(tag_name='Polio Management',
                                              parent_tag_id=ind_tag.id)

        ind_to_tag_batch = [IndicatorToTag(
            **{'indicator_tag_id': sub_tag.id, 'indicator_id': ind.id}) for ind in self.indicators]
        IndicatorToTag.objects.bulk_create(ind_to_tag_batch)

        self.campaign_id = Campaign.objects.create(
            start_date='2016-01-01',
            end_date='2016-01-02',
            campaign_type_id=campaign_type1.id,
            top_lvl_location_id=12907,
            top_lvl_indicator_tag_id=ind_tag.id,
            office_id=self.office_id,
        ).id

        document = Document.objects.create(
            doc_title='test',
            created_by_id=user_id,
            guid='test')

        self.ss = SourceSubmission.objects.create(
            document_id=document.id,
            submission_json='',
            row_number=0,
            data_date='2016-01-01'
        ).id

    def model_df_to_data(self, model_df, model):

        meta_ids = []

        non_null_df = model_df.where((notnull(model_df)), None)
        list_of_dicts = non_null_df.transpose().to_dict()

        for row_ix, row_dict in list_of_dicts.iteritems():

            row_id = model.objects.create(**row_dict)
            meta_ids.append(row_id)

        return meta_ids

    def create_raw_datapoints(self):

        for row_ix, row_data in self.test_df.iterrows():

            dp_id = self.create_datapoint(row_data.location_id, row_data
                                          .data_date, row_data.indicator_id, row_data.value)

    # def create_datapoint(self, **kwargs):
    def create_datapoint(self, location_id, data_date, indicator_id, value):
        '''
        Right now this is being performed as a database insert.  I would like to
        Test this against the data entry resource, but this will do for now
        in order to test caching.
        '''

        document_id = Document.objects.get(doc_title='test').id
        ss_id = SourceSubmission.objects.get(document_id=document_id).id
        dp = DataPoint.objects.create(
            location_id=location_id,
            data_date=data_date,
            indicator_id=indicator_id,
            campaign_id=self.campaign_id,
            value=value,
            cache_job_id=-1,
            source_submission_id=ss_id,
            unique_index=str(location_id) + str(data_date) +
            str(self.campaign_id) + str(indicator_id)
        )

        return dp

    def test_location_aggregation(self):
        '''
        Using the calc_data.csv, create a test_df and target_df.  Ensure that
        the aggregation and calcuation are working properly, but ingesting the
        stored data, running the cache, and checking that the calculated data
        for the aggregate location (parent location, in this case Nigeria) is as
        expected.

        In addition to the datapoints in the test file, i insert a null valu
        to ensure that any null won't corrpupt the calculation.

        python manage.py test rhizome.tests.test_agg.AggRefreshTestCase.test_location_aggregation --settings=rhizome.settings.test

        '''
        self.create_raw_datapoints()

        indicator_id, data_date, raw_location_id,\
            agg_location_id, null_location_id, NaN_location_id = \
            22, '2016-01-01', 12910, 12907, 12928, 12913

        location_ids = Location.objects.filter(
            parent_location_id=agg_location_id).values_list('id', flat=True)

        DataPoint.objects.filter(
            indicator_id=indicator_id,
            # data_date = data_date,
            location_id=null_location_id
        ).update(value=None)

        DataPoint.objects.filter(
            indicator_id=indicator_id,
            # data_date = data_date,
            location_id=NaN_location_id
        ).update(value='NaN')

        dps = DataPoint.objects.filter(
            indicator_id=indicator_id,
            # data_date = data_date,
            location_id__in=location_ids,
            value__isnull=False
        ).values_list('id', 'value')

        sum_dp_value = sum([y for x, y in dps if not isnan(y)])

        AggRefresh(self.campaign_id)

        #################################################
        ## ensure that raw data gets into AggDataPoint ##
        #################################################

        raw_value = DataPoint.objects.get(
            # data_date = data_date,
            indicator_id=indicator_id,
            location_id=raw_location_id)\
            .value

        ind_obj = Indicator.objects.get(id=indicator_id)

        raw_value_in_agg = AggDataPoint.objects.get(
            # data_date = data_date,
            indicator_id=indicator_id,
            location_id=raw_location_id)\
            .value

        self.assertEqual(raw_value, raw_value_in_agg)

        #############################################
        ## ensure that the aggregated data gets in ##
        #############################################

        loc_tree_df = DataFrame(list(LocationTree.objects.all().values()))
        agg_df = DataFrame(list(AggDataPoint.objects.filter(\
            indicator_id=indicator_id,\
            campaign_id=self.campaign_id
        ).values()))

        # print loc_tree_df[loc_tree_df['parent_location_id'] ==\
        #     agg_location_id]
        # print '=== agg_dp df === %s ' % agg_location_id
        # print agg_df

        agg_value = AggDataPoint.objects.get(
            indicator_id=indicator_id,
            campaign_id=self.campaign_id,
            location_id=agg_location_id
        ).value

        self.assertEqual(agg_value, sum_dp_value)

        ######################################################
        ## ensure that any raw data will override aggregate ##
        ######################################################

        override_value = 909090
        agg_override_dp = self.create_datapoint(agg_location_id, data_date,
                                                indicator_id, override_value)

        AggRefresh(self.campaign_id)

        override_value_in_agg = AggDataPoint.objects.get(
            campaign_id=self.campaign_id,
            indicator_id=indicator_id,
            location_id=agg_location_id).value

        self.assertEqual(override_value, override_value_in_agg)

        ###########################################
        # ensure that percentages do not aggregate
        ###########################################

        pct_ind = Indicator.objects.create(
            name='pct missed',
            short_name='pct_missed',
            description='missed pct',
            data_format='pct',
            source_name='my brain',
        )

        dp_1 = DataPoint.objects.create(
            indicator_id=pct_ind.id,
            location_id=location_ids[0],
            campaign_id=self.campaign_id,
            data_date=data_date,
            value=.2,
            source_submission_id=self.ss,
            unique_index=1

        )

        dp_2 = DataPoint.objects.create(
            indicator_id=pct_ind.id,
            location_id=location_ids[1],
            campaign_id=self.campaign_id,
            data_date=data_date,
            value=.6,
            source_submission_id=self.ss,
            unique_index=2

        )

        AggRefresh(self.campaign_id)

        try:
            agg_dp_qs = AggDataPoint.objects.get(
                location_id=agg_location_id,
                indicator_id=pct_ind,
                campaign_id=self.campaign_id,
            )

            error_ocurred = False
        except AggDataPoint.DoesNotExist:
            error_ocurred = True

        self.assertTrue(error_ocurred)

    def test_raw_data_to_computed(self):
        '''
        This just makes sure that any data in the datapoint table, gets into the
        Calculated DataPoint table.  That is, i insert a value for missed
        children in Borno, the same exact data should be in the
        datapoint_with_computed table no matter what.
        '''

        self.create_raw_datapoints()
        indicator_id, data_date, raw_location_id,\
            agg_location_id, campaign_id = 22, '2016-01-01', 12910, 12907, 1

        location_ids = Location.objects.filter(
            parent_location_id=agg_location_id).values_list('id', flat=True)

        dp_values = DataPoint.objects.filter(
            indicator_id=indicator_id,
            data_date=data_date,
            location_id__in=location_ids
        ).values_list('value', flat=True)

        sum(dp_values)

        AggRefresh(self.campaign_id)

        ############################################################
        ## ensure that raw data gets into datapoint_with_computed ##
        ############################################################

        raw_value = DataPoint.objects.get(data_date=data_date,
                                          indicator_id=indicator_id,
                                          location_id=raw_location_id)\
            .value

        raw_value_in_agg = DataPointComputed.objects.get(
            campaign_id=self.campaign_id,
            indicator_id=indicator_id,
            location_id=raw_location_id)\
            .value

        self.assertEqual(raw_value, raw_value_in_agg)

    def test_sum_and_pct(self):
        '''
        The system uses the "PART_TO_BE_SUMMED" edge type in order to create
        indicators such that the sum of:
          - Number Missed
          - Missed due to other reasons(24)
          - Child Absent(251)
          - Not in Plan (267)
          - Not Visited (268)
          - Non Compliance(264)

        gives us: All Missed Children (21)
        as well as: pct missed children due to refusal (166)

        Here we create new metadata so we can test this functionality for an
        Abstracted use case and test that

        1.  We can SUM indicators
        2.  We can use the result of #2 as the denominator for a percentage
            calculation.
        '''
        Indicator.objects.all().delete()

        data_date, location_id, agg_location_id = '2016-01-01', 12910, 12907
        val_1, val_2, val_3 = 303, 808, 909
        ## create the parent and sub indicators ##
        parent_indicator = Indicator.objects.create(
            name='Number of Avoidable Deaths',
            short_name='Number of Avoidable Deaths',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=parent_indicator.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_1 = Indicator.objects.create(
            name='Number of Deaths due to Conflict',
            short_name='Number of Deaths due to Conflict',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_1.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_2 = Indicator.objects.create(
            name='Number of Deaths due to Malaria',
            short_name='Number of Deaths due to Malaria',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_2.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_3 = Indicator.objects.create(
            name='Number of Deaths due to Hunger',
            short_name='Number of Deaths due to Hunger',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_3.id,
                                           campaign_id=self.campaign_id)

        pct_indicator = Indicator.objects.create(
            name='pct of Deaths due to Hunger',
            short_name='pct of Deaths due to Hunger',
            data_format='pct'
        )
        CampaignToIndicator.objects.create(indicator_id=pct_indicator.id,
                                           campaign_id=self.campaign_id)

        ## FOR SUM OF PARTS CALUCLATIONS ##
        indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_1.id,
            calculation='PART_TO_BE_SUMMED'
        )
        indicator_calc_2 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_2.id,
            calculation='PART_TO_BE_SUMMED'
        )
        indicator_calc_3 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_3.id,
            calculation='PART_TO_BE_SUMMED'
        )

        ## FOR PART OVER WHOLE CALCULATIONS ##
        indicator_calc_numerator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_indicator.id,
            indicator_component_id=sub_indicator_3.id,
            calculation='NUMERATOR'
        )
        indicator_calc_denominator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_indicator.id,
            indicator_component_id=parent_indicator.id,
            calculation='DENOMINATOR'
        )

        ss_id = SourceSubmission.objects.all()[0].id
        ## create the datapoints ##
        dp_1 = DataPoint.objects.create(
            indicator_id=sub_indicator_1.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_1,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=1
        )
        dp_2 = DataPoint.objects.create(
            indicator_id=sub_indicator_2.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_2,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=2

        )
        dp_3 = DataPoint.objects.create(
            indicator_id=sub_indicator_3.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_3,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=3

        )

        AggRefresh(self.campaign_id)

        calc_value_sum = DataPointComputed.objects.get(
            indicator_id=parent_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id
        ).value

        calc_value_pct = DataPointComputed.objects.get(
            indicator_id=pct_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id
        ).value

        # test SUM calculation
        sum_target_value = val_1 + val_2 + val_3
        self.assertEqual(calc_value_sum, sum_target_value)

        # test part over whole calction
        pct_target_value = val_3 / float(sum_target_value)
        self.assertEqual(calc_value_pct, pct_target_value)

    def test_part_of_difference(self):
        '''
        see here: rhizome.work/manage_system/manage/indicator/187

        We use this calculation to perform the following calculation:

        WHOLE_OF_DIFFERENCE(x) - PART_OF_DIFFERENCE(y)
        -----------------------------------------
             WHOLE_OF_DIFFERENCE(x)
        '''

        data_date, location_id, agg_location_id = '2016-01-01', 12910, 12907
        x, y = 303.00, 808.00

        ## create the parent and sub indicators ##
        parent_indicator = Indicator.objects.create(
            name='Refsual Conversion',
            short_name='Refsual Conversion',
            data_format='pct'
        )
        CampaignToIndicator.objects.create(indicator_id=parent_indicator.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_part = Indicator.objects.create(
            name='Refusals After Revisit',
            short_name='Refusals After Revisit',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_part.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_denom = Indicator.objects.create(
            name='Refusals Before Revisit',
            short_name='Refusals Before Revisit',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_denom.id,
                                           campaign_id=self.campaign_id)

        ## FOR SUM OF PARTS CALUCLATIONS ##
        indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_part.id,
            calculation='PART_OF_DIFFERENCE'
        )
        indicator_calc_3 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_denom.id,
            calculation='WHOLE_OF_DIFFERENCE'
        )

        ss_id = SourceSubmission.objects.all()[0].id
        ## create the datapoints ##
        dp_1 = DataPoint.objects.create(
            indicator_id=sub_indicator_denom.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=x,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=1

        )
        dp_2 = DataPoint.objects.create(
            indicator_id=sub_indicator_part.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=y,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=2

        )

        AggRefresh(self.campaign_id)

        calc_value = DataPointComputed.objects.get(
            indicator_id=parent_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id
        ).value

        # test SUM calculation
        target_value = (x - y) / x
        self.assertEqual(round(calc_value, 4), round(target_value, 4))

    def test_missing_part_of_sum(self):
        data_date, location_id, agg_location_id = '2016-01-01', 12910, 12907
        val_1, val_2 = 101, 102
        ## create the parent and sub indicators ##
        parent_indicator = Indicator.objects.create(
            name='Number of Missing Children',
            short_name='Number of Avoidable Deaths',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=parent_indicator.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_1 = Indicator.objects.create(
            name='Number Missing Due to Refusal',
            short_name='Number Missing Due to Refusal',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_1.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_2 = Indicator.objects.create(
            name='Number Missing Due to Absence',
            short_name='Number Missing Due to Absence',
            data_format='int'
        )
        sub_indicator_3 = Indicator.objects.create(
            name='Number Missing Due to ??',
            short_name='Number Missing Due to ??',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_3.id,
                                           campaign_id=self.campaign_id)

        indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_1.id,
            calculation='PART_TO_BE_SUMMED'
        )
        indicator_calc_2 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_2.id,
            calculation='PART_TO_BE_SUMMED'
        )

        indicator_calc_3 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_3.id,
            calculation='PART_TO_BE_SUMMED'
        )
        ss_id = SourceSubmission.objects.all()[0].id
        ## create the datapoints. We're only adding data points for ##
        ## two of the three datapoints that are mapped as parts to be summed ##
        dp_1 = DataPoint.objects.create(
            indicator_id=sub_indicator_1.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_1,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=1

        )
        dp_2 = DataPoint.objects.create(
            indicator_id=sub_indicator_2.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_2,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=2

        )
        AggRefresh(self.campaign_id)

        calc_value_sum = DataPointComputed.objects.get(
            indicator_id=parent_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id
        ).value

        sum_target_value = val_1 + val_2
        self.assertEqual(calc_value_sum, sum_target_value)

    def test_recursive_sum(self):
        '''
        Consider the case in which we have "number of missed children" which is
        the sum of "missed children due to absence", "missed children due to
        refusal", and "missed children due to child absence."

        Now consider that "missed children due to refusal" is also generated
        from the sum of "refusal due to religious reasons", "refusal due to
        too many rounds", "refusal due to - unhappy with team " (see more here:
        http://rhizome.work/manage_system/manage/indicator/264).

        There are two levels here and this test aims to cover this use case.
        '''

        data_date, location_id = '2016-01-01', 12910

        Indicator.objects.all().delete()

        parent_indicator = Indicator.objects.create(
            name='Number of Avoidable Deaths',
            short_name='Number of Avoidable Deaths',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=parent_indicator.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_1 = Indicator.objects.create(
            name='Number of Deaths due to Conflict',
            short_name='Number of Deaths due to Conflict',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_1.id,
                                           campaign_id=self.campaign_id)

        sub_sub_indicator_1 = Indicator.objects.create(
            name='Number Conflict Deaths - Children',
            short_name='Conflict Deaths - Children',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_sub_indicator_1.id,
                                           campaign_id=self.campaign_id)

        sub_sub_indicator_2 = Indicator.objects.create(
            name='Number of Adult Civilian Deaths',
            short_name='Number of Adult Civilian Deaths',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_sub_indicator_2.id,
                                           campaign_id=self.campaign_id)

        sub_sub_indicator_3 = Indicator.objects.create(
            name='Number of Conflict Deaths - Militants',
            short_name='Conflict Deaths - Militants',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_sub_indicator_3.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_2 = Indicator.objects.create(
            name='Number of Deaths due to Malaria',
            short_name='Number of Deaths due to Malaria',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_2.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_2_sub_1 = Indicator.objects.create(
            name='Number of Deaths due to Malaria -- Child had No Net',
            short_name='Number of Deaths due to Malaria -- no net',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_2_sub_1.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_2_sub_2 = Indicator.objects.create(
            name='Number of Deaths due to Malaria -- Child had No Medicine',
            short_name='Number of Deaths due to Malaria -- no Medicie',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_2_sub_2.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_3 = Indicator.objects.create(
            name='Number of Deaths due to Hunger',
            short_name='Number of Deaths due to Hunger',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_3.id,
                                           campaign_id=self.campaign_id)

        ## FOR SUM OF PARTS CALUCLATIONS ##
        indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_1.id,
            calculation='PART_TO_BE_SUMMED'
        )
        indicator_calc_2 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_2.id,
            calculation='PART_TO_BE_SUMMED'
        )
        indicator_calc_3 = CalculatedIndicatorComponent.objects.create(
            indicator_id=parent_indicator.id,
            indicator_component_id=sub_indicator_3.id,
            calculation='PART_TO_BE_SUMMED'
        )

        ## 2nd layer of indicator calculation ##
        sub_indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=sub_indicator_1.id,
            indicator_component_id=sub_sub_indicator_1.id,
            calculation='PART_TO_BE_SUMMED'
        )
        sub_indicator_calc_2 = CalculatedIndicatorComponent.objects.create(
            indicator_id=sub_indicator_1.id,
            indicator_component_id=sub_sub_indicator_2.id,
            calculation='PART_TO_BE_SUMMED'
        )
        sub_indicator_calc_3 = CalculatedIndicatorComponent.objects.create(
            indicator_id=sub_indicator_1.id,
            indicator_component_id=sub_sub_indicator_3.id,
            calculation='PART_TO_BE_SUMMED'
        )

        ## 2nd layer of indicator calculation ##
        sub_indicator_calc_1 = CalculatedIndicatorComponent.objects.create(
            indicator_id=sub_indicator_2.id,
            indicator_component_id=sub_indicator_2_sub_1.id,
            calculation='PART_TO_BE_SUMMED'
        )
        sub_indicator_calc_2 = CalculatedIndicatorComponent.objects.create(
            indicator_id=sub_indicator_2.id,
            indicator_component_id=sub_indicator_2_sub_2.id,
            calculation='PART_TO_BE_SUMMED'
        )

        ## create all the datapoints ##

        values_to_insert = {
            sub_indicator_2.id: 33,
            sub_indicator_3.id: 44,
            sub_sub_indicator_1.id: 44,
            sub_sub_indicator_2.id: 55,
            sub_sub_indicator_3.id: 66,
            sub_indicator_2_sub_1.id: 77,
            sub_indicator_2_sub_2.id: 88,
        }

        for k, v in values_to_insert.iteritems():
            self.create_datapoint(location_id, data_date, k, v)

        AggRefresh(self.campaign_id)

        parent_indicator_target_value = sum(values_to_insert.values())
        parent_indicator_1_actual_value = DataPointComputed.objects.get(
            location_id=location_id,
            indicator_id=parent_indicator,
        ).value

        self.assertEqual(parent_indicator_1_actual_value,
                         parent_indicator_target_value)

        # test that a parent overrides the sum of its children when there
        ## are multiple levels of indicator calcuations ##
        sub_2_target_val = values_to_insert[sub_indicator_2.id]
        sub_2_actual_val = DataPointComputed.objects.get(
            location_id=location_id,
            indicator_id=sub_indicator_2.id,
        ).value

        self.assertEqual(sub_2_target_val, sub_2_actual_val)

    def test_boolean_aggregation(self):

        # create a boolean indicato
        boolean_indicator = Indicator.objects.create(
            name='Is Controlled by "Anti Governemnt Elements"',
            short_name='Is at War',
            data_format='bool'
        )

        # find the locations for which we should store raw data.. For instance
        # if it is 'district is at war', then we dont expect data stored at
        # the porivnce level.  Here though, we get all children of a particluar
        # parent.
        locations = Location.objects.filter(
            parent_location_id=self.top_lvl_location.id)

        # split the data into 1 value being fale, the rest being trye.
        # this aludes to the fact that the parent location shoul dhave a value
        # that is somethign like [ 1 / data.length() ]

        false_loc_id = locations[0].id
        true_loc_list = locations[1:]

        ## create the true and false datapoints ##
        false_datapoint = DataPoint.objects.create(
            campaign_id=self.campaign_id,
            location_id=false_loc_id,
            indicator_id=boolean_indicator.id,
            source_submission_id=self.ss,
            value=0
        )

        true_datapoint_batch = [DataPoint(**{
            'campaign_id': self.campaign_id,
            'location_id': loc.id,
            'indicator_id': boolean_indicator.id,
            'source_submission_id': self.ss,
            'value': 1,
            'unique_index': str(self.campaign_id) + str(boolean_indicator.id) + str(loc.id)
        }) for loc in true_loc_list]
        DataPoint.objects.bulk_create(true_datapoint_batch)

        # run the agg refresh ( this is the code that will actually transofrm
        # the booleans to numerics. )
        AggRefresh(self.campaign_id)

        # now get the expected aggrgated data and compare it with the percentage
        # value that we expect given how we split up the locations above.
        dwc_value = DataPointComputed.objects.get(
            location_id=self.top_lvl_location.id,
            campaign_id=self.campaign_id,
            indicator=boolean_indicator.id
        ).value

        expected_value = 1 - (1.0 / len(locations))
        self.assertEqual(expected_value, dwc_value)

    def test_calculated_indicator_agg(self):
        Indicator.objects.all().delete()

        data_date, agg_location_id = '2016-01-01', 12907
        child_locations = Location.objects.filter(
            parent_location_id=agg_location_id)
        location_id = child_locations[0].id
        location_id_2 = child_locations[1].id

        ## create the parent and sub indicators ##
        parent_indicator = Indicator.objects.create(
            name='Number of Avoidable Deaths',
            short_name='Number of Avoidable Deaths',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=parent_indicator.id,
                                           campaign_id=self.campaign_id)

        sub_indicator_1 = Indicator.objects.create(
            name='Number of Deaths due to Conflict',
            short_name='Number of Deaths due to Conflict',
            data_format='int'
        )
        CampaignToIndicator.objects.create(indicator_id=sub_indicator_1.id,
                                           campaign_id=self.campaign_id)

        pct_indicator = Indicator.objects.create(
            name='pct of Deaths due to Conflict',
            short_name='pct of Deaths due to Conflict',
            data_format='pct'
        )
        CampaignToIndicator.objects.create(indicator_id=pct_indicator.id,
                                           campaign_id=self.campaign_id)

        ## FOR PART OVER WHOLE CALCULATIONS ##
        indicator_calc_numerator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_indicator.id,
            indicator_component_id=sub_indicator_1.id,
            calculation='NUMERATOR'
        )
        indicator_calc_denominator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_indicator.id,
            indicator_component_id=parent_indicator.id,
            calculation='DENOMINATOR'
        )

        val_1 = 32
        val_2 = 100

        val_1_loc_2 = 48
        val_2_loc_2 = 200

        ss_id = SourceSubmission.objects.all()[0].id
        ## create the datapoints ##
        dp_1 = DataPoint.objects.create(
            indicator_id=sub_indicator_1.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_1,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=1

        )

        dp_2 = DataPoint.objects.create(
            indicator_id=parent_indicator.id,
            data_date=data_date,
            location_id=location_id,
            campaign_id=self.campaign_id,
            value=val_2,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=2

        )

        dp_1_loc_2 = DataPoint.objects.create(
            indicator_id=sub_indicator_1.id,
            data_date=data_date,
            location_id=location_id_2,
            campaign_id=self.campaign_id,
            value=val_1_loc_2,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=3

        )

        dp_2_loc_2 = DataPoint.objects.create(
            indicator_id=parent_indicator.id,
            data_date=data_date,
            location_id=location_id_2,
            campaign_id=self.campaign_id,
            value=val_2_loc_2,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=4

        )

        AggRefresh(self.campaign_id)

        calc_value_pct = DataPointComputed.objects.get(
            indicator_id=pct_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id
        ).value

        calc_value_pct_2 = DataPointComputed.objects.get(
            indicator_id=pct_indicator.id,
            campaign_id=self.campaign_id,
            location_id=location_id_2
        ).value

        # test part over whole calculation for child locations
        pct_target_value = val_1 / float(val_2)
        self.assertEqual(calc_value_pct, pct_target_value)

        pct_target_value_2 = val_1_loc_2 / float(val_2_loc_2)
        self.assertEqual(calc_value_pct_2, pct_target_value_2)

        # make sure that part over whole aggregates as well
        total_dp = DataPointComputed.objects.get(
            indicator_id=parent_indicator.id,
            campaign_id=self.campaign_id,
            location_id=agg_location_id).value

        self.assertEqual(total_dp, val_2 + val_2_loc_2)

        try:

            pct_dp = DataPointComputed.objects.get(
                indicator_id=pct_indicator.id,
                campaign_id=self.campaign_id,
                location_id=agg_location_id).value

        except ObjectDoesNotExist:
            fail("aggregation did not work")

        self.assertEqual(round(pct_dp, 5), round(
            (val_1 + val_1_loc_2) / float(val_2 + val_2_loc_2), 5))

    def test_multiple_calculations(self):

        num_seen = Indicator.objects.create(
            name='number children seen',
            short_name='number children seen',
            data_format='int'
        )

        num_vacc = Indicator.objects.create(
            name='number children vaccinated',
            short_name='number children vaccinated',
            data_format='int'
        )

        num_missed = Indicator.objects.create(
            name='number children missed',
            short_name='number children missed',
            data_format='int'
        )

        pct_missed = Indicator.objects.create(
            name='pct childrent missed',
            short_name='pct children missed',
            data_format='pct'
        )

        indicator_calc_numerator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_missed.id,
            indicator_component_id=num_missed.id,
            calculation='NUMERATOR'
        )

        indicator_calc_denominator = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_missed.id,
            indicator_component_id=num_seen.id,
            calculation='DENOMINATOR'
        )

        indicator_calc_part_of_diff = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_missed.id,
            indicator_component_id=num_vacc.id,
            calculation='PART_OF_DIFFERENCE'
        )
        indicator_calc_part_of_whole = CalculatedIndicatorComponent.objects.create(
            indicator_id=pct_missed.id,
            indicator_component_id=num_seen.id,
            calculation='WHOLE_OF_DIFFERENCE'
        )

        num_missed_val = 45.0
        num_seen_val = 100.0
        num_vacc_val = 55.0

        ss_id = SourceSubmission.objects.all()[0].id

        dp_num_missed = DataPoint.objects.create(
            indicator_id=num_missed.id,
            location_id=self.top_lvl_location.id,
            campaign_id=self.campaign_id,
            value=num_missed_val,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=3
        )

        dp_num_seen = DataPoint.objects.create(
            indicator_id=num_seen.id,
            location_id=self.top_lvl_location.id,
            campaign_id=self.campaign_id,
            value=num_seen_val,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=4
        )

        AggRefresh(self.campaign_id)

        # check that numerator and denominator option work
        cdp_pct_missed_1 = DataPointComputed.objects.filter(
            indicator_id=pct_missed.id)[0]
        self.assertEqual(cdp_pct_missed_1.value,
                         num_missed_val / float(num_seen_val))

        dp_num_vaccinated = DataPoint.objects.create(
            indicator_id=num_vacc.id,
            location_id=self.top_lvl_location.id,
            campaign_id=self.campaign_id,
            value=num_vacc_val,
            source_submission_id=ss_id,
            cache_job_id=-1,
            unique_index=5
        )

        AggRefresh(self.campaign_id)
        # check that this works when we can do whole/part of difference
        cdp_pct_missed_2 = DataPointComputed.objects.filter(
            indicator_id=pct_missed.id)[0]
        1.0 - float(num_vacc_val) / float(num_seen_val)

        self.assertEqual(cdp_pct_missed_2.value, 0.45)

        # check that this works when we can only do whole/part of difference
        DataPoint.objects.filter(indicator_id=num_missed.id).delete()

        AggRefresh(self.campaign_id)
        cdp_pct_missed_3 = DataPointComputed.objects.filter(
            indicator_id=pct_missed.id)[0]
        self.assertEqual(cdp_pct_missed_3.value, 0.45)
