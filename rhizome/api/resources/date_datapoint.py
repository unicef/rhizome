

import itertools
from pandas import DataFrame, concat, notnull
from django.http import HttpResponse

from tastypie import fields
from tastypie.utils.mime import build_content_type

from rhizome.api.serialize import CustomSerializer
from rhizome.api.resources.base_model import BaseModelResource

from rhizome.models import DataPointComputed, Campaign, Location,\
    LocationPermission, LocationTree, IndicatorClassMap, Indicator, DataPoint, \
    CalculatedIndicatorComponent, LocationType
import math


class DateDatapointResource(BaseModelResource):
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

    indicator_id = fields.IntegerField(attribute='indicator_id', null=True)
    location_id = fields.IntegerField(attribute='location_id')

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


        # NOTE this needs to be cleaned up and any many of these methonds
        # should be executed by the parent ( base model resource )
        using the DataPoint as the object_class
        '''

        resource_name = 'date_datapoint'  # cooresponds to the URL of the resource
        object_class = DataPoint
        max_limit = None  # return all rows by default ( limit defaults to 20 )
        serializer = CustomSerializer()

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(DateDatapointResource, self).__init__(*args, **kwargs)
        self.error = None
        self.parsed_params = None

    def get_response_meta(self, request, objects):

        meta = super(BaseModelResource, self)\
            .get_response_meta(request, objects)

        chart_uuid = request.GET.get('chart_uuid', None)
        if chart_uuid:
            meta['chart_uuid'] = chart_uuid

        ind_id_list = request.GET.get('indicator__in', '').split(',')
        meta['location_ids'] = self.location_ids
        meta['indicator_ids'] = ind_id_list
        meta['campaign_ids'] = self.campaign_id_list

        return meta

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


        self.parsed_params = self.parse_url_params(request.GET)

        self.time_gb = self.parsed_params['group_by_time']
        self.base_data_df = self.group_by_time_transform(request)

        ## if no datapoints, we return an empty list#
        if len(self.base_data_df) == 0:
            return []

        # ## fill in missing data if requested ##
        # if self.parsed_params['show_missing_data'] == u'1':
        #     df = self.add_missing_data(self.base_data_df)
        #     self.base_data_df = df.where((notnull(df)),None)

        return self.base_data_df.to_dict('records')

    def get_time_group_series(self, dp_df):


        if self.time_gb == 'year':
            dp_df['time_grouping'] = dp_df[
                'data_date'].map(lambda x: int(x.year))
        elif self.time_gb == 'quarter':
            dp_df['time_grouping'] = dp_df['data_date']\
                .map(lambda x: str(x.year) + str((x.month - 1) // 3 + 1))
        elif self.time_gb == 'all_time':
            dp_df['time_grouping'] = 1
        else:
            dp_df = DataFrame()

        ## find the unique possible groupings for this time range and gb param
        ## sketchy -- this wont work for quarter groupingings, only years.
        distinct_time_groupings = list(dp_df.time_grouping.unique())
        if not distinct_time_groupings:
            start_yr, end_yr = self.parsed_params['start_date'][0:4],\
                self.parsed_params['end_date'][0:4]
            distinct_time_groupings = range(int(start_yr), int(end_yr))

        self.parsed_params['campaign__in'] = distinct_time_groupings
        self.campaign_id_list = distinct_time_groupings

        return dp_df

    def build_location_tree(self, request):
        '''
        Find out the data you are trying to return for ... in use case #1,
        this would be all of the provinces in afghanistan.. for #2 it would be
        all of the districts.  This is important because we will use
        these to group by in addition to the time_grouping and indicator
        later on.  Furthermore, since the location tree table has all of
        the possible combinations of ancestry, we want to make sure that
        when we perform operations on it, that it is small as possible.

        The output of this function is a Data Frame that looks like:

            location_id, parent_location_id
            | NY State      | USA       |
            | California    | USA       |
            | NY City       | NY State  |
            | The Bronx     | NY City   |


        If the depth_level = 0, it means that we want to query for only the
        location that is in the location_id parameter, so we return somethign
        like:

            location_id, parent_location_id
            | The Bronx | The Bronx |

        '''


        requested_location_id = int(self.parsed_params['location_id__in'])
        depth_level = int(self.parsed_params['location_depth'])

        if depth_level == 0:
            self.location_ids = [ requested_location_id ]
            return DataFrame([[requested_location_id,requested_location_id]], \
                columns = ['location_id', 'parent_location_id'])

        # what is the admin level of the requested location #
        parent_location_admin_level =  Location.objects\
            .filter(id = requested_location_id)\
            .values_list('location_type__admin_level',flat=True)[0]

        # what is the location_type of the keys we need to return
        # calculated by the admin_level of the requested ( see above )
        # and the depth level in the request
        location_type_id_of_parent_keys = LocationType.objects\
            .get(admin_level = parent_location_admin_level + depth_level).id

        # get the relevant parent / child heirarchy
        loc_tree_df = DataFrame(list(LocationTree.objects
                          .filter(parent_location__location_type_id =\
                            location_type_id_of_parent_keys)
                          .values_list('location_id', 'parent_location_id')),
                     columns=['location_id', 'parent_location_id'])

        self.location_ids = list(loc_tree_df['location_id'].unique())

        return loc_tree_df

    def group_by_time_transform(self, request):
        '''
            Imagine the following location tree heirarchy
            ( Country -> Region -> Province -> District )

            Based on these two queries return the coorseponding result
                1. Show Polio cases in Afghanistan with a bubble on each
                    province
                2. Show Polio cases in Afghanistan with a bubble on each
                    district
                2. Show Polio cases in the southern Region with a bubble
                    on each district
        '''

        dp_df_columns = ['data_date', 'indicator_id', 'location_id', 'value']

        # HACKK for situational dashboard
        if self.parsed_params['chart_uuid'] ==\
                '5599c516-d2be-4ed0-ab2c-d9e7e5fe33be':

            return self.handle_polio_case_table(dp_df_columns)

        cols = ['data_date', 'indicator_id', 'location_id', 'value']

        ## build the location heirarchy for the requested locations #
        loc_tree_df = self.build_location_tree(request)
                ## now find the data for the children of those parents
        dp_df = DataFrame(list(DataPoint.objects.filter(
                location_id__in = list(loc_tree_df['location_id'].unique()),
                indicator_id__in = self.parsed_params['indicator__in']
            ).values(*cols)), columns=cols)

        if len(dp_df) == 0:
            return []

        dp_df = self.get_time_group_series(dp_df)
        merged_df = dp_df.merge(loc_tree_df)

        ## sum all values for locations with the same parent location
        gb_df = DataFrame(merged_df
                          .groupby(['indicator_id', 'time_grouping', 'parent_location_id'])['value']
                          .sum())\
            .reset_index()

        gb_df = gb_df.rename(columns={
            'parent_location_id': 'location_id',
            'time_grouping': 'campaign_id' ## should change this in the FE
            })

        gb_df = gb_df.rename(columns={'parent_location_id': 'location_id'})

        return gb_df

    def handle_polio_case_table(self, dp_df_columns):
        '''
        This is a very specific peice of code that allows us to generate a table
        with
            - date of latest case
            - infected district count
            - infected province count
        THis relies on certain calcluations to be made in
        caluclated_indicator_component.
        '''
        # http://localhost:8000/api/v1/datapoint/?indicator__in=37,39,82,40&location_id__in=1&campaign_start=2015-04-26&campaign_end=2016-04-26&chart_type=RawData&chart_uuid=1775de44-a727-490d-adfa-b2bc1ed19dad&group_by_time=year&format=json
        calc_indicator_data_for_polio_cases = CalculatedIndicatorComponent.\
            objects.filter(indicator__name='Polio Cases').values()

        if len(calc_indicator_data_for_polio_cases) > 0:
            self.ind_meta = {'base_indicator':
                             calc_indicator_data_for_polio_cases[
                                 0]['indicator_id']
                             }
        else:
            self.ind_meta = {}

        for row in calc_indicator_data_for_polio_cases:
            calc = row['calculation']
            ind_id = row['indicator_component_id']
            self.ind_meta[calc] = ind_id

        parent_location_id = self.parsed_params['location_id__in']

        all_sub_locations = LocationTree.objects.filter(
            parent_location_id=parent_location_id
        ).values_list('location_id', flat=True)

        flat_df = DataFrame(list(DataPoint.objects.filter(
            location_id__in=all_sub_locations,
            indicator_id__in=self.parsed_params['indicator__in']
        ).values(*dp_df_columns)), columns=dp_df_columns)

        flat_df = self.get_time_group_series(flat_df)
        flat_df['parent_location_id'] = parent_location_id

        gb_df = DataFrame(flat_df
                          .groupby(['indicator_id', 'time_grouping', 'parent_location_id'])
                          ['value']
                          .sum())\
            .reset_index()

        latest_date_df = DataFrame(flat_df
                                   .groupby(['indicator_id', 'time_grouping'])['data_date']
                                   .max())\
            .reset_index()
        latest_date_df['value'] = latest_date_df['data_date']\
            .map(lambda x: x.strftime('%Y-%m-%d'))
        latest_date_df['indicator_id'] = self\
            .ind_meta['latest_date']

        district_count_df = DataFrame(flat_df
                                      .groupby(['time_grouping']).location_id
                                      .nunique())\
            .reset_index()
        district_count_df['value'] = district_count_df['location_id']
        district_count_df['indicator_id'] = self\
            .ind_meta['district_count']

        concat_df = concat([gb_df, latest_date_df,  district_count_df])
        concat_df[['indicator_id', 'value', 'time_grouping', 'data_date']]
        concat_df['parent_location_id'] = parent_location_id
        concat_df = concat_df.drop('location_id', 1)
        concat_df = concat_df.rename(
            columns={'parent_location_id': 'location_id'})
        return concat_df

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        objects = self.get_object_list(bundle.request)
        if not objects:
            objects = []
        return objects


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
            'group_by_time': None, 'chart_uuid': None, 'location_depth': None
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

        return parsed_params
