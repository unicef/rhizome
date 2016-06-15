import traceback
import itertools

from django.http import HttpResponse

from tastypie import http
from tastypie.resources import Resource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import Resource
from tastypie.utils.mime import build_content_type

from pandas import DataFrame

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.resources.base_resource import BaseResource

from rhizome.models import LocationPermission, Location, LocationTree, \
    LocationType, Campaign, DataPointComputed, Indicator


class BaseDataPointResource(BaseResource):
    '''
    '''
    class Meta(BaseResource.Meta):
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()

    #################################################
    ### date_datapoint / campaign_datapoint helpter methods ###
    #################################################

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

        list_of_lists = [\
            self.parsed_params['indicator__in'],\
            self.location_ids,\
            self.parsed_params['campaign__in']\
        ]
        cart_product = list(itertools.product(*list_of_lists))
        cart_prod_df = DataFrame(cart_product)

        ## for date_datapoint, we convert the "time grouping" to campaign ##
        columns_list = ['indicator_id','location_id', 'campaign_id']

        cart_prod_df.columns = columns_list
        cart_prod_df['value'] = None

        if len(df) == 0: ## if no datapoints, just return cart product DF ##
            return cart_prod_df

        df = cart_prod_df.merge(df, how='left', on=columns_list)

        df["value"] = df["value_y"]
        df.drop("value_x", axis=1, inplace=True)
        df.drop("value_y", axis=1, inplace=True)

        return df

    def create_response(self, request, data, response_class=HttpResponse,
                        **response_kwargs):
        """
        This is overridden from tastypie.  The point here is to be able to
        Set the content-disposition header for csv downloads.

        That is the only instance in which this override should change the
        response is if the desired format is csv.

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


    def get_datapoint_response_meta(self, request, objects):
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

        return parsed_params

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
