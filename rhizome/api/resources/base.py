import traceback

from tastypie import http
from tastypie.resources import Resource

from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import Resource

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.exceptions import DatapointsException

from rhizome.models import LocationPermission, Location, LocationTree, \
    LocationType, Campaign, DataPointComputed, Indicator
from django.http import HttpResponse

class BaseResource(Resource):
    '''
    '''
    class Meta:
        authentication = MultiAuthentication(CustomSessionAuthentication(), ApiKeyAuthentication())
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
                    location__location_type_id = loc_type_id,
                    parent_location_id__in = location_ids
                ).values_list('location_id', flat=True)

            elif 'location_depth' in request.GET:
                return_locations =[]
                for location_id in location_ids:
                    # this can probably be condensed into fewer queries...
                    parent_location_type = Location.objects.get(id = location_id).location_type_id
                    parent_admin_level = LocationType.objects.get(id = parent_location_type).admin_level
                    location_depth = int(request.GET['location_depth'])
                    descendant_location_type = LocationType.objects.get(admin_level= parent_admin_level + location_depth)
                    descendant_ids = LocationTree.objects.filter(
                        location__location_type_id = descendant_location_type.id,
                        parent_location_id = location_id
                        ).values_list('location_id', flat=True)
                    return_locations.extend(descendant_ids)
                return return_locations

            else:
                return location_ids
        else:
            return Location.objects.all().values_list('id', flat=True)

    def dispatch(self, request_type, request, **kwargs):
        """
        Overrides Tastypie and calls get_list.
        """

        try:
            self.top_lvl_location_id = LocationPermission.objects.get(
                user_id = request.user.id).top_lvl_location_id
        except LocationPermission.DoesNotExist:
            self.top_lvl_location_id = Location.objects\
                .filter(parent_location_id = None)[0].id

        allowed_methods = getattr(self._meta, "%s_allowed_methods" % request_type, None)
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
