import numpy as np
import sys
from pandas import DataFrame, pivot_table, notnull

from django.http import HttpResponse

from tastypie import fields
from tastypie.utils.mime import build_content_type
from tastypie.exceptions import NotFound

from datapoints.api.serialize import CustomSerializer
from datapoints.api.resources.base_non_model import BaseNonModelResource
from datapoints.api.functions import get_locations_to_return_from_url

from datapoints.models import DataPointComputed, Campaign, Location,\
    LocationPermission


class ResultObject(object):
    '''
    This is the same as a row in the CSV export in which one row has a distinct
    location / campaign combination, and the remaing columns represent the
    indicators requested.  Indicators are a list of IndicatorObjects.
    '''
    location = None
    campaign = None
    indicators = list()


class DatapointResource(BaseNonModelResource):
    '''
    This is the class that coincides with the /api/v1/datapoint endpoint.
    '''

    error = None
    parsed_params = {}
    location = fields.IntegerField(attribute='location')
    campaign = fields.IntegerField(attribute='campaign')
    indicators = fields.ListField(attribute='indicators')

    class Meta(BaseNonModelResource.Meta):
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

        object_class = ResultObject  # use the class above to define response
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
        ## put this in base class ##
        self.top_lvl_location_id = LocationPermission.objects.get(
            user_id = request.user.id).top_lvl_location_id

        results = []

        err = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return []

        self.location_ids = get_locations_to_return_from_url(request)

        # Pivot the data on request instead of caching ##
        # in the datapoint_abstracted table ##
        df_columns = ['id', 'indicator_id', 'campaign_id', 'location_id', 'value']
        dwc_df = DataFrame(
            list(DataPointComputed.objects.filter(
                campaign__in=self.parsed_params['campaign__in'],
                location__in=self.location_ids,
                indicator__in=self.parsed_params['indicator__in'])
                .values_list(*df_columns)), columns=df_columns)

        try:
            p_table = pivot_table(
                dwc_df, values='value', index=['indicator_id'], columns=['location_id', 'campaign_id'], aggfunc=np.sum)
            no_nan_pivoted_df = p_table.where((notnull(p_table)), None)
            pivoted_data = no_nan_pivoted_df.to_dict()

            #### we need two dictionaries, one that has the value of the datapoint_computed object and one with the id ##

            p_table_for_id = pivot_table(
                dwc_df, values='id', index=['indicator_id'], columns=['location_id', 'campaign_id'], aggfunc=np.sum)
            no_nan_pivoted_df_for_id = p_table_for_id.where((notnull(p_table)), None)
            pivoted_data_for_id = no_nan_pivoted_df_for_id.to_dict()

        except KeyError: ## there is no data
            if len(self.parsed_params['campaign__in']) > 1: ## implicit way to only do this for data entry
                return

            pivoted_data, pivoted_data_for_id = {}, {}
            for location_id in self.location_ids:
                tupl = (location_id, self.parsed_params['campaign__in'][0])
                pivoted_data[tupl] = {}
                pivoted_data_for_id[tupl] = {}

        for row, indicator_dict in pivoted_data.iteritems():

            indicator_objects = [{
                'indicator': unicode(k),
                'computed': pivoted_data_for_id[row][k],
                'value': v
            } for k, v in indicator_dict.iteritems()]

            # avail_indicators = set([x for x,y in indicator_dict.keys()])
            missing_indicators = list(set(self.parsed_params['indicator__in']))
            for ind in missing_indicators:
                if ind not in indicator_dict.keys():
                    indicator_objects.append({'indicator': ind, 'value': None, 'computed_id': None})

            r = ResultObject()
            r.location = row[0]
            r.campaign = row[1]
            r.indicators = indicator_objects
            results.append(r)

        return results

    def obj_get_list(self, bundle, **kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        # get one object from data source
        pk = int(kwargs['pk'])
        try:
            return bundle.data[pk]
        except KeyError:
            raise NotFound("Object not found")

    def alter_list_data_to_serialize(self, request, data):
        '''
        If there is an error for this resource, add that to the response.  If
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well
        '''

        try:
            chart_type = request.GET['chart_type']
        except KeyError:
            chart_type = None

        if chart_type == 'TableChart':
            p_loc_qs = Location.objects\
                .filter(id__in = self.location_ids)\
                .values('name','parent_location__name')

            data['meta']['parent_location_list'] = [l for l in p_loc_qs]
            data['meta']['default_sort_order'] = [l['name'] for l in p_loc_qs]

        data['meta']['campaign_list'] = [c for c in self.campaign_qs.values()]

        # add errors if it exists
        if self.error:
            data['error'] = self.error
        else:
            data['error'] = None

        return data

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
            'campaign__in': None, 'location__in': None}

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

        if self.top_lvl_location_id == 4721: ## hack to get sherine off my back
            campaign_qs = Campaign.objects.filter(
                start_date__gte=campaign_start,
                start_date__lte=campaign_end
                # top_lvl_location_id=self.top_lvl_location_id
            )

        else:
            campaign_qs = Campaign.objects.filter(
                start_date__gte=campaign_start,
                start_date__lte=campaign_end,
                top_lvl_location_id=self.top_lvl_location_id
            )

        campaign__in = [c.id for c in campaign_qs]

        return campaign__in
