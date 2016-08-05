import traceback

from django.http import HttpResponse

from tastypie import http
from tastypie.resources import Resource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication, MultiAuthentication

from rhizome.api.serialize import CustomSerializer
from rhizome.api.custom_session_authentication import CustomSessionAuthentication
from rhizome.api.custom_cache import CustomCache
from rhizome.api.exceptions import RhizomeApiException

from rhizome.models.location_models import LocationPermission, Location

class BaseResource(Resource):
    '''
    https://github.com/django-tastypie/django-tastypie/blob/master/tastypie/resources.py
    '''

    class Meta:
        authentication = MultiAuthentication(
            CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()

    ### Tastypie Methods ###
    def __init__(self, api_name=None):
        '''
        In Rhizome, all user permissinos are bound by the top level location
        that they can see.  For instance, if i am the head of Zika data analysis
        in the Bahia Province of Brazil, that woul be my top level location.

        The top_lvl_location_id is used in the `get_locations_to_return_from_url`
        function, so that for shapes, locatinos and datapoints the user only
        can see what they are permissioned to.

        This is an additional parameter needed by the rhizome API to behave
        properly.  This variable is set in the dispatch method.
        '''

        self.top_lvl_location_id = None

        return super(BaseResource, self).__init__(api_name=None)

    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.
        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.
        """
        return self.get_object_list(request).filter(**applicable_filters)

    def get_object_list(self, request):
        """
        An ORM-specific implementation of ``get_object_list``.
        Returns a queryset that may have been limited by other overrides.
        """
        return super(BaseResource, self).get_object_list(self, request)

    def obj_get_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.
        ``GET`` dictionary of bundle.request can be used to narrow the query.
        """
        return super(BaseResource, self).obj_get_list(bundle, **kwargs)

    def save(self, bundle, skip_errors=False):

        return super(BaseResoruce, self).save(bundle, skip_errors)

    def lookup_kwargs_with_identifiers(self, bundle, kwargs):
        """
        Kwargs here represent uri identifiers Ex: /repos/<user_id>/<repo_name>/
        We need to turn those identifiers into Python objects for generating
        lookup parameters that can find them in the DB
        """
        return super(BaseResource, self)\
            .lookup_kwargs_with_identifiers(bundle, kwargs)

    def rollback(self, bundles):
        """
        A ORM-specific implementation of ``rollback``.
        Given the list of bundles, delete all models pertaining to those
        bundles.
        """
        return super(BaseResource, self).rolback(bundles)

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.
        By default, it uses this resource's ``detail_uri_name`` in order to
        create the URI.
        """
        return super(BaseResource, self).detail_uri_kwargs(bundle_or_obj)

    ############################
    ## Custom Rhizome Methods ##
    ############################

    def validate_filters(self, request):
        '''
        Make sure that all required filters have been passed in
        '''

        filters = {}

        # Grab a mutable copy of the request#
        if hasattr(request, 'GET'):
            filters = request.GET.copy()

        # check required parameters and raise exception if one is missing #
        if hasattr(self._meta, 'GET_params_required'):
            keys_req = self._meta.GET_params_required
            missing_keys = list(set(keys_req).difference(set(filters.keys())))
            if len(missing_keys) > 0:
                msg = 'Missing required parameter %s' % missing_keys[0]
                raise RhizomeApiException(msg)

        return filters

    def dispatch(self, request_type, request, **kwargs):
        """
        Overrides Tastypie and calls get_list for GET, obj_create for POST,
        get_detail and obj_delete when fetching or delete an object with
        primary key requested
        """

        try:
            self.top_lvl_location_id = LocationPermission.objects.get(
                user_id=request.user.id).top_lvl_location_id
        except LocationPermission.DoesNotExist:
            self.top_lvl_location_id = Location.objects\
                .filter(parent_location_id=None)[0].id

        allowed_methods = getattr(
            self._meta, "%s_allowed_methods" % request_type, None)

        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']

        request_method = self.method_check(request, allowed=allowed_methods)
        method = getattr(self, "%s_%s" % (request_method, request_type), None)

        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            response = method(request, **kwargs)
        # except RhizomeApiException as error: ## use more specific exception.
        except Exception as error: ## use more specific exception.
            data = {
                'traceback': traceback.format_exc(),
                'error': error.message,
                # 'code': error.code
            }
            return self.error_response(
                request,
                data,
                response_class=http.HttpApplicationError
           )

        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()

        return response

    def get_response_meta(self, request, objects):
        '''
        needs to get cleaned up. need to be able to subclass this in
        order to add additional k,v pairs to the meta depending on
        which level we are att in the class heirarchy
        '''

        meta = {
            'get_params': request.GET,
            'top_lvl_location_id': self.top_lvl_location_id,
            'limit': None,  # paginator.get_limit(),
            'offset': None,  # paginator.get_offset(),
            'total_count': len(objects),
        }

        return meta
