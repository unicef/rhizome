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
from rhizome.api.exceptions import DatapointsException

from rhizome.models import LocationPermission, Location, LocationTree, \
    LocationType, Campaign, DataPointComputed, Indicator



class BaseResource(Resource):
    '''
    '''
    class Meta:
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()

    def get_locations_to_return_from_url(self, request):
        '''
        This method is used in both the /geo and /datapoint endpoints.  Based
        on the values parsed from the URL parameters find the locations needed
        to fulfill the request based on the four rules below.

        TO DO -- Check Location Permission so that the user can only see
        What they are permissioned to.
        '''

        if 'location_id__in' in request.GET:
            location_ids = map(int, request.GET['location_id__in'].split(','))

            if 'location_type' in request.GET:
                loc_type_id = int(request.GET['location_type'])
                return LocationTree.objects.filter(
                    location__location_type_id=loc_type_id,
                    parent_location_id__in=location_ids
                ).values_list('location_id', flat=True)

            elif 'location_depth' in request.GET:
                return_locations = []
                for location_id in location_ids:
                    # this can probably be condensed into fewer queries...
                    parent_location_type = Location.objects.get(
                        id=location_id).location_type_id
                    parent_admin_level = LocationType.objects.get(
                        id=parent_location_type).admin_level
                    location_depth = int(request.GET['location_depth'])
                    descendant_location_type = LocationType.objects.get(
                        admin_level=parent_admin_level + location_depth)
                    descendant_ids = LocationTree.objects.filter(
                        location__location_type_id=descendant_location_type.id,
                        parent_location_id=location_id
                    ).values_list('location_id', flat=True)
                    return_locations.extend(descendant_ids)

                location_ids = return_locations

        else:
            location_ids =  Location.objects.all().values_list('id', flat=True)

        try:
            request.GET['filter_indicator']
            location_ids = self.get_locations_from_filter_param(location_ids)
        except KeyError:
            pass

        return location_ids

    def get_locations_from_filter_param(self, location_ids):
        '''
        '''

        value_filter = self.parsed_params['filter_value'].split(',')

        location_ids = DataPointComputed.objects.filter(
            campaign__in = self.parsed_params['campaign__in'],
            location__in = location_ids,
            indicator__short_name =  self.parsed_params['filter_indicator'],
            value__in = value_filter)\
                .values_list('location_id', flat=True)

        return location_ids

    def dispatch(self, request_type, request, **kwargs):
        """
        Overrides Tastypie and calls get_list.
        """

        try:
            self.top_lvl_location_id = LocationPermission.objects.get(
                user_id=request.user.id).top_lvl_location_id
        except LocationPermission.DoesNotExist:
            self.top_lvl_location_id = Location.objects\
                .filter(parent_location_id=None)[0].id

        allowed_methods = getattr(
            self._meta, "%s_allowed_methods" % request_type, None)
        #
        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']

        request_method = self.method_check(request, allowed=allowed_methods)
        method = getattr(self, "%s_%s" % (request_method, request_type), None)

        # if method is None:
        #     raise ImmediateHttpResponse(response=http.HttpNotImplemented())

        self.is_authenticated(request)
        self.throttle_check(request)
        # All clear. Process the request.

        # If what comes back isn't a ``HttpResponse``, assume that the
        # request was accepted and that some action occurred. This also
        # prevents Django from freaking out.

        # request = convert_post_to_put(request)

        try:
            response = method(request, **kwargs)
        except Exception as error:

            error_code = DatapointsException.defaultCode
            error_message = DatapointsException.defaultMessage

            if isinstance(error, DatapointsException):
                error_code = error.code
                error_message = error.message

            data = {
                'traceback': traceback.format_exc(),
                'error': error_message,
                'code': error_code
            }

            return self.error_response(
                request,
                data,
                response_class=http.HttpApplicationError
            )

        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()

        return response

    #################################################
    ### raw_datapoint / datapoint helpter methods ###
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


    def get_response_meta(self, request, objects):

        meta_dict = {
            'top_lvl_location_id': self.top_lvl_location_id,
            'limit': None,  # paginator.get_limit(),
            'offset': None,  # paginator.get_offset(),
            'total_count': len(objects),
        }
        return meta_dict

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
