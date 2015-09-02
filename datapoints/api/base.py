from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from tastypie.resources import ModelResource, Resource, ALL
from tastypie.cache import SimpleCache

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func


from datapoints.models import RegionType,Region,RegionPermission

class CustomAuthentication(Authentication):
    '''
    Super Simple permissions check to ensure user is logged in.  Futher
    permissions are appled for GET and POST for the datapoitn resource
    based on the regional and indicator level permission of the user found
    in the request.
    '''

    def is_authenticated(self, request, **kwargs):
        '''
        If the user is logged in, return True else return False...
        '''

        if request.user.id:
            return True

        return False

class CustomCache(SimpleCache):
    '''
    Set up to override the simple cache method in order to customize the
    behavior of the cache control headers.
    '''

    def cache_control(self):
        '''
        Instatiate the cache_control instance, and add the headers needed.
        '''
        control = super(CustomCache, self).cache_control()
        control.update({'must_revalidate':True, 'max_age': 3600})
        return control


class BaseModelResource(ModelResource):
    '''
    This applies to only the V1 API.  This method inherits from Tastypie's
    model resource.

    This resource strips down almost all of the tastypie functions which
    drastically slow down the API performance.

    IMPORTANT: if you note, all of the resources use the .values() option for
    each queryset.  That returns the model as JSON, so the idea is that the
    API does not need to serialize or dehydrate the resource.

    The models are set up so that the API does as little transformation as
    possible.  That means however, that a few of our metadata models ( see
    campaign / indicator ) are cached and contain related information making
    the job of the API easy.
    '''

    class Meta():
        authentication = CustomAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        allowed_methods = ['get','post','put','patch', 'delete']
        filtering = {
            "id": ALL,
        }
        cache = CustomCache()


    def dispatch(self, request_type, request, **kwargs):
        """
        Overrides Tastypie and calls get_list.  For now, that makes these
        resources GET only. ( no POST / PUT / PATCH ).
        """

        response = self.get_list(request, **kwargs)

        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()

        return response

    def get_list(self, request, **kwargs):
        """
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(), limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [obj for obj in to_be_serialized[self._meta.collection_name]]

        return self.create_response(request, bundles)

class BaseNonModelResource(Resource):
    '''
    NOTE: This applies to only the V1 API.  This is only used for the
    /api/v1/datapoint endpoint.

    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta():
        authentication = CustomAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        cache = CustomCache()
