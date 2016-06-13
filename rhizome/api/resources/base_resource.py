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

from rhizome.models import LocationPermission, Location, LocationTree, \
    LocationType, DataPointComputed

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

    def obj_get(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get``.
        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        return super(BaseResource, self).obj_get(bundle, **kwargs)

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """

        print '===\n' * 10
        print bundle
        print '===\n' * 10

        return self.save(bundle)


    def save(self, bundle, skip_errors=False):
        print '==saving=='

        if bundle.via_uri:
            return bundle

        self.is_valid(bundle)

        if bundle.errors and not skip_errors:
            raise ImmediateHttpResponse(response=self.error_response(bundle.request, bundle.errors))

        # Check if they're authorized.
        if bundle.obj.pk:
            self.authorized_update_detail(self.get_object_list(bundle.request), bundle)
        else:
            self.authorized_create_detail(self.get_object_list(bundle.request), bundle)

        # Save FKs just in case.
        self.save_related(bundle)

        # Save the main object.
        obj_id = self.create_identifier(bundle.obj)

        if obj_id not in bundle.objects_saved or bundle.obj._state.adding:
            bundle.obj.save()
            bundle.objects_saved.add(obj_id)

        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)
        return bundle

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

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        """
        A ORM-specific implementation of ``obj_update``.
        """
        return super(BaseResource, self)\
            .obj_update(bundle, skip_errors=False, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete_list``.
        """
        return super(BaseResource, self)\
            .obj_delete_list(bundle, **kwargs)

    def obj_delete_list_for_update(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete_list_for_update``.
        """
        return super(BaseResource, self)\
            .obj_delete_list_for_update(self, bundle, **kwargs)

    def obj_delete(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete``.

        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        return super(BaseResource, self).obj_delete(bundle, **kwargs)

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
        except RhizomeApiException as error: ## use more specific exception.

            data = {
                'traceback': traceback.format_exc(),
                'error': error.message,
                'code': error.code
            }

            return self.error_response(
                request,
                data,
                response_class=http.HttpApplicationError
            )

        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()

        return response

    def get_response_meta(self, objects):

        meta_dict = {
            'top_lvl_location_id': self.top_lvl_location_id,
            'limit': None,  # paginator.get_limit(),
            'offset': None,  # paginator.get_offset(),
            'total_count': len(objects),
        }
        return meta_dict
