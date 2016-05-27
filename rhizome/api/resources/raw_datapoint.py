import numpy as np
import sys
import itertools
from pandas import DataFrame, pivot_table, notnull, concat
from django.http import HttpResponse

from tastypie import fields
from tastypie.utils.mime import build_content_type
from tastypie.exceptions import NotFound

from rhizome.api.serialize import CustomSerializer
from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.custom_logic import handle_polio_case_table

from rhizome.models import DataPointComputed, Campaign, Location,\
    LocationPermission, LocationTree, IndicatorClassMap, Indicator, DataPoint, \
    CalculatedIndicatorComponent

import math
from datetime import datetime

class DatapointResource(BaseModelResource):
    '''
    - **GET Requests:**
        - *Required Parameters:*
            'indicator__in' A comma-separated list of indicator IDs to fetch. By default, all indicators
            'chart_type'
        - *Optional Parameters:*
            'location__in' A comma-separated list of location IDs
            'campaign_start' format: ``YYYY-MM-DD``  Include only datapoints from campaigns that began on or after the supplied date
            'campaign_end' format: ``YYYY-MM-DD``  Include only datapoints from campaigns that ended on or before the supplied date
            'campaign__in'   A comma-separated list of campaign IDs. Only datapoints attached to one of the listed campaigns will be returned
            'cumulative'
    '''

    error = None
    parsed_params = {}
    indicator_id = fields.IntegerField(attribute='indicator_id', null=True)
    campaign_id = fields.IntegerField(attribute='campaign_id', null=True)
    data_date = fields.DateField(attribute='data_date', null=True)
    computed_id = fields.IntegerField(attribute='computed_id', null=True)
    location_id = fields.IntegerField(attribute='location_id')
    value = fields.CharField(attribute='value', null=True)

    class Meta(BaseModelResource.Meta):
        '''
        As this is a NON model resource, we must specify the object_class
        that will represent the data returned to the applicaton.  In this case
        as specified by the ResultObject the fields in our response will be
        location_id, campaign_id, indcator_json.
        The resource name is datapoint, which means this resource is accessed
        by /api/v1/datapoint/.
        The data is serialized by the CustomSerializer which uses the default
        handler for JSON responses and transforms the data to csv when the
        user clicks the "download data" button on the data explorer.
        note - authentication inherited from parent class
        '''

        # object_class = ResultObject  # use the class above to define response
        resource_name = 'datapoint'  # cooresponds to the URL of the resource
        max_limit = None  # return all rows by default ( limit defaults to 20 )
        serializer = CustomSerializer()

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(DatapointResource, self).__init__(*args, **kwargs)
        self.error = None
        self.parsed_params = None

    def create_response(self, request, data, response_class=HttpResponse,
                        **response_kwargs):
        """
        THis is overridden from tastypie.  The point here is to be able to
        Set the content-disposition header for csv downloads.  That is the only
        instance in which this override should change the response is if the
        desired format is csv.
        The content-disposition header allows the user to save the .csv
        to a directory of their chosing.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)

        response = response_class(content=serialized,
            content_type=build_content_type(desired_format),**response_kwargs)

        if desired_format == 'text/csv':
            response['Content-Disposition'] = 'attachment; filename=polio_data.csv'
            response.set_cookie('dataBrowserCsvDownload', 'true')

        return response

    def get_object_list(self, request):
        '''
        This is where the action happens in this resource.  AFter passing the
        url paremeters, get the list of locations based on the parameters passed
        in the url as well as the permissions granted to the user responsible
        for the request.
        Using the location_ids from the get_locations_to_return_from_url method
        we query the datapoint abstracted table, then iterate through these
        values cleaning the indicator_json based in the indicator_ids passed
        in the url parameters, and creating a ResultObject for each row in the
        response.
        '''

        self.error = None
        self.class_indicator_map = self.build_class_indicator_map();

        results = []
        err = self.parse_url_params(request.GET)
        if err:
            self.error = err
            return []

        self.location_ids = self.get_locations_to_return_from_url(request)
        time_gb = self.parsed_params['group_by_time']
        if time_gb == 'campaign' or time_gb is None:
            return self.base_transform()
        else:
            self.base_data_df = self.group_by_time_transform()

        return self.transform_df_to_results(self.base_data_df)

    def get_time_group_series(self, dp_df):
        time_grouping = self.parsed_params['group_by_time']
        if time_grouping == 'year':
            dp_df['time_grouping'] = dp_df['data_date'].map(lambda x: int(x.year))
        elif time_grouping == 'quarter':
            dp_df['time_grouping'] = dp_df['data_date']\
                .map(lambda x: str(x.year) + str((x.month-1) // 3 + 1))
        elif time_grouping == 'all_time':
            dp_df['time_grouping'] = 1
        else:
            dp_df = DataFrame()
        self.parsed_params['campaign__in'] = list(dp_df.time_grouping.unique())
        return dp_df


    def transform_df_to_results(self, df):
        # the following line is a hack. TODO: figure out where empty list is being returned from
        if type(df) == list:
            return []
        if self.parsed_params['show_missing_data'] == u'1':
            df = self.add_missing_data(df)
        if 'campaign_id' in df.columns:
            df = df.sort('campaign_id')
        else:
            df = df.sort('time_grouping')
        results =[]
        df.apply(self.df_to_result_obj, args=(results,), axis=1)
        return results

    def group_by_time_transform(self):
        dp_df_columns = ['data_date','indicator_id','location_id','value']
        time_grouping =  self.parsed_params['group_by_time']

        # HACKK for situational dashboard
        if self.parsed_params['chart_uuid'] ==\
            '5599c516-d2be-4ed0-ab2c-d9e7e5fe33be':

            self.parsed_params['show_missing_data'] = 1
            return handle_polio_case_table(self, dp_df_columns)

        cols = ['data_date','indicator_id','location_id','value']
        dp_df = DataFrame(list(DataPoint.objects.filter(
            location_id__in = self.location_ids,
            indicator_id__in = self.parsed_params['indicator__in']
        ).values(*cols)),columns=cols)

        if not dp_df.empty:
            dp_df = self.get_time_group_series(dp_df)
            gb_df = DataFrame(dp_df\
                .groupby(['indicator_id','time_grouping','location_id'])['value']\
                .sum())\
                .reset_index()
            return gb_df

        # need to recurse down to a subloaction with data
         # if the data isn't available at the current level
        else:
            depth_level, max_depth, sub_location_ids = 0, 3, self.location_ids
            while dp_df.empty and depth_level < max_depth:
                sub_location_ids = Location.objects\
                    .filter(parent_location_id__in=sub_location_ids)\
                    .values_list('id', flat=True)

                dp_df = DataFrame(list(DataPoint.objects.filter(
                    location_id__in = sub_location_ids,
                    indicator_id__in = self.parsed_params['indicator__in']
                ).values(*cols)),columns=cols)
                depth_level += 1

            dp_df = self.get_time_group_series(dp_df)
            if dp_df.empty:
                return []
            location_tree_df = DataFrame(list(LocationTree.objects\
                .filter(location_id__in = sub_location_ids)\
                .values_list('location_id','parent_location_id')),\
                    columns=['location_id','parent_location_id'])

            merged_df = dp_df.merge(location_tree_df)

            filtered_df = merged_df[merged_df['parent_location_id']\
                .isin(self.location_ids)]

            # sum all values for locations with the same parent location
            gb_df = DataFrame(filtered_df\
                .groupby(['indicator_id','time_grouping','parent_location_id'])['value']\
                .sum())\
                .reset_index()

            gb_df = gb_df.rename(columns={'parent_location_id' : 'location_id'})
            return gb_df

    def df_to_result_obj(self, row, results_list):

        dp = ResultObject()
        if not math.isnan(row['indicator_id']):
            dp.indicator_id = row['indicator_id']
        if 'campaign_id' in row:
            dp.campaign_id = row['campaign_id']
        else:
            dp.campaign_id = row['time_grouping']
        dp.location_id = row['location_id']
        if not (isinstance(row['value'], float) and math.isnan(row['value'])):
            dp.value = row['value']
        results_list.append(dp)


    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        objects = self.get_object_list(bundle.request)
        if not objects:
            objects = []
        return objects

    def get_response_meta(self, request, objects):
        '''
        If there is an error for this resource, add that to the response.  If
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well
        '''

        meta = {}

        try:
            location_ids = request.GET['location_id__in']
            meta['location_ids'] = location_ids
        except KeyError:
            location_ids = None

        try:
            indicator_ids = request.GET['indicator__in']
            meta['indicator_ids'] = indicator_ids
        except KeyError:
            indicator_ids = None

        try:
            chart_uuid = request.GET['chart_uuid']
            meta['chart_uuid'] = chart_uuid
        except KeyError:
            indicator_ids = None

        meta['campaign_ids'] = self.parsed_params['campaign__in']
        meta['total_count'] = len(objects)

        return meta

    def dehydrate(self, bundle):
        '''
        This method allws me to remove or add information to each data object,
        for instance the resource_uri.
        '''

        bundle.data.pop('resource_uri')

        return bundle

    # #########################
    # ### HELPER METHODS #####
    # #########################

    def parse_url_params(self, query_dict):
        '''
        For the query dict return another dictionary ( or error ) in accordance
        to the expected ( both required and optional ) parameters in the request
        URL.
        '''
        parsed_params = {}

        required_params = {'indicator__in': None}

        # try to find optional parameters in the dictionary. If they are not
        # there return the default values ( given in the dict below)
        optional_params = {
            'the_limit': 10000, 'the_offset': 0, 'agg_level': 'mixed',
            'campaign_start': '2012-01-01', 'campaign_end': '2900-01-01',
            'campaign__in': None, 'location__in': None,'location_id__in':None,\
            'filter_indicator':None, 'filter_value': None,\
            'show_missing_data':None, 'cumulative':0, \
             'group_by_time': None, 'chart_uuid': None
        }

        for k, v in optional_params.iteritems():
            try:
                parsed_params[k] = query_dict[k]
            except KeyError:
                parsed_params[k] = v

        for k, v in required_params.iteritems():

            try:
                parsed_params[k] = [int(p) for p in query_dict[k].split(',')]
            except KeyError as err:
                err_msg = '%s is a required parameter!' % err
                return err_msg, None

        campaign_in_param = parsed_params['campaign__in']

        if campaign_in_param:
            campaign_ids = [int(c_id) for c_id in campaign_in_param.split(',')]


        else:
            campaign_ids = self.get_campaign_list(
                parsed_params['campaign_start'], parsed_params['campaign_end']
            )
        self.campaign_qs = Campaign.objects.filter(id__in=campaign_ids)
        parsed_params['campaign__in'] = campaign_ids

        self.parsed_params = parsed_params

        return None

    def get_campaign_list(self, campaign_start, campaign_end):
        '''
        Based on the parameters passed for campaigns, start/end or __in
        return to the parsed params dictionary a list of campaigns to query
        '''

        campaign_qs = Campaign.objects.filter(
            start_date__gte=campaign_start,
            start_date__lte=campaign_end,
            top_lvl_location_id=self.top_lvl_location_id
        )

        return [c.id for c in campaign_qs]

    def build_class_indicator_map(self):
        query_results = IndicatorClassMap.objects.filter(is_display=True) \
            .values_list('indicator','enum_value','string_value')
        class_indicator_map ={}
        for query in query_results:
            if query[0] not in class_indicator_map:
                class_indicator_map[query[0]] ={}
            class_indicator_map[query[0]][query[1]] = query[2]

        return class_indicator_map

    def add_class_indicator_val(self, x):
        ind_id = x['indicator_id']
        ind_val = x['value']
        if ind_id in self.class_indicator_map and ind_val in self.class_indicator_map[ind_id]:
            new_val = self.class_indicator_map[ind_id][ind_val]
            x['value'] = new_val
        return x

    def base_transform(self):
        results = []

        response_fields = ['id', 'indicator_id', 'campaign_id', 'location_id',\
            'value']

        results = list(DataPointComputed.objects.filter(
                campaign__in=self.parsed_params['campaign__in'],
                location__in=self.location_ids,
                indicator__in=self.parsed_params['indicator__in'])\
                .values(*response_fields))

        ## fill in missing data if requested ##
        if self.parsed_params['show_missing_data'] == u'1':
            df = self.add_missing_data(DataFrame(results))
            df = df.where((notnull(df)),None)
            results = df.to_dict('records')

        ## add enumeration for 'class' indicators
        if 'class' in Indicator.objects\
            .filter(id__in = self.parsed_params['indicator__in'])\
            .values_list('data_format', flat=True):

            df = DataFrame(results).apply(self.add_class_indicator_val, axis=1)
            results = df.to_dict('records')

        return results


    def add_missing_data(self, df):
        '''
        If the campaign / locaiton cobination has no related datapoitns, we
        add the keys here so that we can see the row of data in data entry
        or data browser.

        This in the future can be controlled with a parameter so that for
        instance with a table chart for a large number of districts, we only
        show those with data.

        This is largely for Data entry so that we can see a row in the form
        even when there is no existing data.
        '''


        list_of_lists = [self.parsed_params['indicator__in'], self.location_ids, self.parsed_params['campaign__in']]
        cart_product = list(itertools.product(*list_of_lists))
        cart_prod_df = DataFrame(cart_product)
        if 'campaign_id' in df.columns:
            columns_list = ['indicator_id','location_id', 'campaign_id']
        else:
            columns_list = ['indicator_id','location_id', 'time_grouping']

        cart_prod_df.columns = columns_list
        df = df.merge(cart_prod_df, how='outer', on=columns_list)

        return df
