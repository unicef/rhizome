from django.db import models

from pandas import DataFrame, notnull, concat

from rhizome.models.indicator_models import CalculatedIndicatorComponent
from rhizome.models.location_models import Location, LocationTree
from rhizome.models.office_models import Office
from rhizome.models.indicator_models import IndicatorTag, Indicator

class CampaignType(models.Model):
    '''
    Each campaign must have a campaign_type_id.

    LPD ( low performing district )
    SNID ( Sub National Immunization Day )
    NID ( National Immunization Day )
    Mop Up ( Damage control after a case is found )

    '''

    name = models.CharField(max_length=55)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        db_table = 'campaign_type'


class Campaign(models.Model):
    '''
    A grouping of rhizome.  For polio, for we have a "campaign type" of
    "National Immunization Day" or "Mop Up" which means an immeiate response
    to a case by conncentrated vaccination campaigns in that area.

    The campaign thus allows you to model these two things with the model in
    these two instances:

    1. NID - Happens monthly for the Endemics.  We have a certain type of
    Inticators that we want to collect for this.. see "Management Dashboard."

        - indicator_list = Management Dashboard Indicators
        - top_lvl_location = Afghanistan

    2. Mop Up - Could happen anywhere where low immunity, for instance Ukraine.

        - indicator_list = A few select Indicators related to the "mop up"
        effort.  These will be different, put potentially overlapping from the
        NID indicator list.
        - top_lvl_location = Ukraine

    For other efforts, this model can be useful.. For Routine Immunization
    one could imagine a similar setup.

    The campaign model has a method called "get_datapoints", which gets the
    relevant raw and aggregated datapoints for a given campaign.  The data
    is aggregated from the date, indicator_list and location in the AggRefresh.

    The indicator_list, is determined by taking the flatened top lvl indicator
    tree that is for the campaign.
    '''

    name = models.CharField(max_length=255)
    office = models.ForeignKey(Office)
    campaign_type = models.ForeignKey(CampaignType)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'campaign'
        ordering = ('-start_date',)
        unique_together = ('office', 'start_date')

    def aggregate_and_calculate(self):

        self.dp_columns = ['location_id', 'indicator_id', 'value']
        self.dwc_batch, self.dwc_tuple_dict = [], {}

        self.agg_datapoints()
        self.calc_datapoints()

    def agg_datapoints(self):
        '''
        Regional Aggregation based on the adjacency list built on top of the
        parent_location_id column.

        Data stored in the DataPoint table for a location with the same
        indicator, campaign will always override the aggregated values, that is
        if the indicator is an integer ( summing percents and booleans
        regionally doesnt make sense.)

        Here, we create a tuple_dict in which the unique key of (locaiton,
        indicator, campaign) represents the key, and the cooresponding value
        is the value.  This way we add to the dict the aggregated values, then
        iterrate through the raw values, adding or updating the data in the
        tuple dict before bulk inserting the data.

        The tuple looks like:  {(1, 201, 164): 12, (2, 101, 168): .24}
        '''

        from rhizome.models.document_models import DataPoint

        agg_dp_batch, tuple_dict = [], {}
        location_tree_columns = ['location_id', 'parent_location_id', 'lvl']

        dp_df = DataFrame(list(DataPoint.objects
                   .filter(campaign_id=self.id)
                   .values_list(*self.dp_columns)), columns=self.dp_columns)

        # NaN to None
        no_nan_dp_df = dp_df.where((notnull(dp_df)), None)

        # find the location ids who's parent's i need to query for
        location_id_list = list(dp_df['location_id'].unique())

        # represents the location heirarchy as a cache from the location table
        location_tree_df = DataFrame(list(LocationTree.objects
          .filter(location_id__in=location_id_list)
          .values_list(*location_tree_columns)), columns=location_tree_columns)

        # join the location tree to the datapoints
        joined_location_df = no_nan_dp_df.merge(location_tree_df)

        # filter the joined dataframe so that we aggregate at the highest
        # level for which there is stored data.  If we do not do this, then
        # if we ingest both, district and province level data, the national
        # will be double the value that it should be.

        # Make sure that the level is not zero, that is that we don't
        # include a row here for the location itself.  Without this filter in
        # the below operation, we wouldn't aggregate anything all.

        max_location_lvl_for_indicator_df = DataFrame(\
            joined_location_df[joined_location_df['lvl'] != 0]\
          .groupby(['indicator_id'])['lvl'].min())  # highest lvl per indicator
        max_location_lvl_for_indicator_df.reset_index(level=0, inplace=True)

        integer_indicators = list(Indicator.objects.filter(
            data_format='int',
            id__in=max_location_lvl_for_indicator_df['indicator_id']
        ).values_list('id', flat=True))

        boolean_indicators = list(Indicator.objects.filter(
            data_format='bool',
            id__in=max_location_lvl_for_indicator_df['indicator_id']
        ).values_list('id', flat=True))


        ## filter df to keep the data for the highest level per indicator ##
        ## meaning, if there is data at both the district and provicne level ##
        ## this line ensures that the country does not take the sum of BOTH
        ## the district and Proivince

        prepped_df = joined_location_df
        # prepped_df = joined_location_df\
        #     .merge(max_location_lvl_for_indicator_df\
        #     , on=['indicator_id', 'lvl'])

        ## FIXME -- need to bring this functioinality back in order to handle
        ## the above.  The idea is that higher level admin data should override
        ## lower level.  This is an edge case and there is no data currently
        ## on production for which this case applies.



        prepped_df['value'] = prepped_df['value'].astype(float)

        ## group by parent_location_id and take the sum ##
        grouped_df_sum = DataFrame(prepped_df
           .groupby(['parent_location_id', 'indicator_id'])['value'].sum())
        grouped_df_mean = DataFrame(prepped_df
            .groupby(['parent_location_id', 'indicator_id'])['value'].mean())

        for ix, dp in grouped_df_sum.iterrows():
            # only aggregate integers ( not boolean or pct )
            if ix[1] in integer_indicators:
                tuple_dict[ix] = dp.value

        for ix, dp in grouped_df_mean.iterrows():
            # get the avg for boolean indicators
            if ix[1] in boolean_indicators:
                tuple_dict[ix] = dp.value

        # now add the raw data to the dict ( overriding agregate if exists )
        for ix, dp in no_nan_dp_df.iterrows():

            if dp.value and dp.value != 'NaN':
                # dont override null value from parent if sum exists for
                # children
                tuple_dict[(dp.location_id, dp.indicator_id)] = dp.value

            if dp.value == 0:
                # pandas treats NaN as zero it seems so do this explicity
                tuple_dict[(dp.location_id, dp.indicator_id)] = dp.value

        ## now prep the batch for the bulk insert ##
        for dp_unique_key, value in tuple_dict.iteritems():

            dp_dict = dict(zip(('location_id', 'indicator_id'), dp_unique_key))

            dp_dict['campaign_id'] = self.id
            dp_dict['value'] = value

            agg_dp_batch.append(AggDataPoint(**dp_dict))

        AggDataPoint.objects.filter(campaign_id=self.id).delete()
        AggDataPoint.objects.bulk_create(agg_dp_batch)

    def calc_datapoints(self):
        '''
        When the agg_datapoint method runs, it will leave the agg_datapoint table
        in a state that all of the rows that were altered, and need to be cached
        thats is the ``calc_refreshed`` column will = 'f' for all of the rows
        that this task effected.

        To find out more about how calculation works, take a look at the
        fn_calc_datapoint stored procedures

        '''

        # the order of these calculations defines their priority, meaning
        # since raw data is the last calculation, this will override all else
        self.sum_of_parts()
        self.part_over_whole()
        self.part_of_difference()
        self.raw_data()
        self.upsert_computed()
        return []

    def build_calc_df(self, calc_list):

        calc_df = DataFrame(list(CalculatedIndicatorComponent.objects
                                 .filter(calculation__in=calc_list)
                                 .values_list('indicator_id', \
            'indicator_component_id', 'calculation')), \
            columns=['calc_indicator_id', 'indicator_component_id', 'calc'])

        return calc_df

    def build_dp_df(self, indicator_id_list):

        dp_df = DataFrame(list(AggDataPoint.objects.all()
                            .filter(indicator_id__in=indicator_id_list
                           .unique(), campaign_id=self.id)
                   .values_list(*self.dp_columns)), columns=self.dp_columns)

        return dp_df

    def join_dp_to_calc(self, calc_df, dp_df):
        '''
        '''

        ## join the above two dataframes in order to determine ##
        ## which indicators require which caluclations ##
        dp_df_with_calc = dp_df.merge(
            calc_df, left_on='indicator_id', right_on='indicator_component_id')

        return dp_df_with_calc

    def build_recursive_sum_calc_df(self, initial_calc_df):
        '''
        TO DO -- handle test_recursive_sum test case
        This only handles one level of recursion.. i.e. the following calc will
        roll up properly.

        "odk missed due to refusal" >> "odk missed total"

        but this one below.. will not:

        "odk missed due to refusal -- male" >> "odk missed due to refusal" >>
        "odk missed total"

        '''

        lvl_1_calc_df = initial_calc_df.merge(initial_calc_df,
          left_on='calc_indicator_id', right_on='indicator_component_id')

        lvl_1_df = lvl_1_calc_df[['calc_indicator_id_y',
                                  'indicator_component_id_x']]

        lvl_1_df.columns = ['calc_indicator_id', 'indicator_component_id']

        lvl_1_df['calc'] = 'PART_TO_BE_SUMMED'
        lvl_1_df['lvl'] = 1
        initial_calc_df['lvl'] = 0

        final_df = concat([initial_calc_df, lvl_1_df])

        return final_df

    def raw_data(self):
        '''
        Add the raw indicator data to the tuple dict.  This happens last so
        the raw indicator data will always override the calculated.
        '''

        for adp in AggDataPoint.objects.filter(campaign_id=self.id):

            adp_tuple = (adp.location_id, adp.indicator_id)
            self.dwc_tuple_dict[adp_tuple] = adp.value

    def sum_of_parts(self):
        '''
        For more info on this see:
        https://github.com/unicef/rhizome/blob/master/docs/spec.rst#aggregation-and-calculation

        '''

        ## get the indicator_ids we need to make the calculation ##
        initial_calc_df = self.build_calc_df(['PART_TO_BE_SUMMED'])

        ## handle recursive calculations ( see spec.rst link above ) ##
        calc_df = self.build_recursive_sum_calc_df(initial_calc_df)

        self_join_calc_df = calc_df.merge(calc_df,\
            left_on='indicator_component_id',\
            right_on='calc_indicator_id',\
            how='left')

        ## get the datapoints for the above indicator_ids ##
        dp_df = self.build_dp_df(calc_df['indicator_component_id'])

        ## now join the above dataframe on itself to set up the calculation ##
        dp_df_with_calc = self.join_dp_to_calc(calc_df, dp_df)

        ## take the sum of all of the component indicators ##
        grouped_df = DataFrame(dp_df_with_calc.merge(dp_df_with_calc)
                       .groupby(['location_id', 'calc_indicator_id'])
                       ['value'].sum())

        for ix, row_data in grouped_df.iterrows():
            self.dwc_tuple_dict[ix] = row_data.value

    def part_over_whole(self):
        '''
        This calculation is dependent on the "sum_of_parts" calculation, so in
        addition to the datapoint_df, we need to get the newly computed
        datapoints from the previous calculation ( dependent_calculation_dp_df )
        '''

        calc_df = self.build_calc_df(['NUMERATOR', 'DENOMINATOR'])

        ## get the datapoints for the above indicator_ids ##
        dp_df = self.build_dp_df(calc_df['indicator_component_id'])

        ## now get a dataframe (dependent_calculation_dp_df) that represents ##
        ## the newly calculated data.  This is necessary because the ##
        ## denominator for the part/whole calculation is often a SUM ##

        dwc_list_of_list = [[k[0], k[1], v] for k, v in
                            self.dwc_tuple_dict.iteritems()]
        dependent_calculation_dp_df = DataFrame(
            dwc_list_of_list, columns=self.dp_columns)
        unioned_dp_df = concat([dp_df, dependent_calculation_dp_df])

        # add the calculation metadata to the df
        dp_df_with_calc = self.join_dp_to_calc(calc_df, unioned_dp_df)

        ## now join the above dataframe on itself to set up the calculation ##
        prepped_for_calc_df = dp_df_with_calc.merge(dp_df_with_calc,
                                on=['location_id', 'calc_indicator_id'])

        # iterate through the dataframe, perform the calculation and add
        # to the dwc_tuple_dict.  ( this could use some clean up )
        for ix, row_data in prepped_for_calc_df.iterrows():

            if row_data.calc_x == 'NUMERATOR' \
                    and row_data.calc_y == 'DENOMINATOR':

                row_tuple = (row_data.location_id, row_data.calc_indicator_id)

                ## this one line is where the calculation happens ##
                try:
                    calculated_value = (row_data.value_x / row_data.value_y)
                except ZeroDivisionError:
                    calculated_value = 0

                self.dwc_tuple_dict[row_tuple] = calculated_value

    def part_of_difference(self):
        '''
        (x - y) / x
        '''

        calc_list = ['WHOLE_OF_DIFFERENCE', 'PART_OF_DIFFERENCE']

        ## get the indicator_ids we need to make the calculation ##
        calc_df = self.build_calc_df(calc_list)

        ## get the datapoints for the above indicator_ids and join with dps ##
        dp_df = self.build_dp_df(calc_df['indicator_component_id'])
        dp_df_with_calc = self.join_dp_to_calc(calc_df, dp_df)

        ## now join the above dataframe on itself to set up the calculation ##
        prepped_for_calc_df = dp_df_with_calc\
            .merge(dp_df_with_calc,on=['location_id', 'calc_indicator_id'])

        # iterrate through the dataframe above, determine the calculated value
        # and finally, create the tuple dict calue for the - calculated data
        for ix, row_data in prepped_for_calc_df.iterrows():

            if row_data.calc_x == 'WHOLE_OF_DIFFERENCE' \
                    and row_data.calc_y == 'PART_OF_DIFFERENCE':

                row_tuple = (row_data.location_id, row_data.calc_indicator_id)

                ## this one line is where the calculation happens ##
                try:
                    calculated_value = (row_data.value_x - row_data.value_y) / \
                        row_data.value_x
                except ZeroDivisionError:
                    calculated_value = 0

                self.dwc_tuple_dict[row_tuple] = calculated_value

    def upsert_computed(self):
        '''
        Using the tuple dict that defined the unique key and associated value
        for the various calculations, prepare this bulk insert, delete the
        existing campaign data then perform the bulk insert.
        '''
        for uq_tuple, val in self.dwc_tuple_dict.iteritems():

            dwc_dict = {'location_id': uq_tuple[0],
                        'indicator_id': uq_tuple[1],
                        'campaign_id': self.id,
                        'value': val
                    }
            self.dwc_batch.append(DataPointComputed(**dwc_dict))
        DataPointComputed.objects.filter(campaign_id=self.id).delete()
        DataPointComputed.objects.bulk_create(self.dwc_batch)

class CampaignToIndicator(models.Model): # FIXME remove this.

    indicator = models.ForeignKey(Indicator)
    campaign = models.ForeignKey(Campaign)

    class Meta:
        db_table = 'campaign_to_indicator'
        unique_together = ('indicator', 'campaign')

class DataPointComputed(models.Model):

    value = models.FloatField()
    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)

    class Meta:
        db_table = 'datapoint_with_computed'
        unique_together = ('location', 'campaign', 'indicator')

class AggDataPoint(models.Model):

    indicator = models.ForeignKey(Indicator)
    location = models.ForeignKey(Location)
    campaign = models.ForeignKey(Campaign)
    value = models.FloatField()

    class Meta:
        db_table = 'agg_datapoint'
        unique_together = ('location', 'campaign', 'indicator')
