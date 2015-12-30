import json
import traceback

from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.middleware.csrf import _sanitize_token, constant_time_compare
from django.utils.http import same_origin

from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication, MultiAuthentication
from tastypie.resources import ModelResource, Resource
from tastypie.cache import SimpleCache
from tastypie import http

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    def csrf_exempt(func):
        return func

from datapoints.models import LocationType, Location, LocationPermission,\
    LocationTree
from datapoints.api.serialize import CustomSerializer


class DataPointsException(Exception):
    defaultMessage = "Sorry, this request could not be processed."
    defaultCode = -1

    def __init__(self, message=defaultMessage, code=defaultCode):
        self.message = message
        self.code = code


class CustomSessionAuthentication(SessionAuthentication):
    """
    """

    def is_authenticated(self, request, **kwargs):
        """
        """

        # this is the line i have to override in order to get
        # POST request to successfully authenticate ##
        if request.method in ('GET', 'POST', 'DELETE'):
            return request.user.is_authenticated()

        if getattr(request, '_dont_enforce_csrf_checks', False):
            return request.user.is_authenticated()

        csrf_token = _sanitize_token(request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))

        if request.is_secure():
            referer = request.META.get('HTTP_REFERER')

            if referer is None:
                return False

            good_referer = 'https://%s/' % request.get_host()

            if not same_origin(referer, good_referer):
                return False

        request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

        if not constant_time_compare(request_csrf_token, csrf_token):
            return False

        return request.user.is_authenticated()


class CustomCache(SimpleCache):
    '''
    Set up to override the simple cache method in order to customize the
    behavior of the cache control headers.
    '''

    def __init__(self, *args, **kwargs):
        super(CustomCache, self).__init__(*args, **kwargs)
        self.request = None
        self.response = None

    def cacheable(self, request, response):
        """
        Returns True or False if the request -> response is capable of being
        cached.
        """
        self.request = request
        self.response = response

        return bool(request.method == "GET" and response.status_code == 200)

    def cache_control(self):
        '''
        Instatiate the cache_control instance, and add the headers needed.
        '''

        cache_control = self.request.META.get('HTTP_CACHE_CONTROL')

        if cache_control is None:
            control = super(CustomCache, self).cache_control()
            control.update({'max_age': self.cache.default_timeout,'s-maxage': self.cache.default_timeout})
            return control
        else:
            self.response['Cache-Control'] = cache_control
            return {}


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

    class Meta:
        authentication = MultiAuthentication(CustomSessionAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get', 'post', 'delete']
        cache = CustomCache()
        serializer = CustomSerializer()

    def dispatch(self, request_type, request, **kwargs):
        """
        Overrides Tastypie and calls get_list.
        """

        self.top_lvl_location_id = LocationPermission.objects.get(
            user_id = request.user.id).top_lvl_location_id

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

            error_code = DataPointsException.defaultCode
            error_message = DataPointsException.defaultMessage

            if isinstance(error, DataPointsException):
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

    def get_list(self, request, **kwargs):
        """
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        bundles = []

        # this is a temporary hack to get data_entry working ##
        # long term fix is to make DataPointEntryResource a NonModelResource
        # https://trello.com/c/skxxpzYj/327-rp-bug-2005-cannot-load-entry-form-in-enter-data-via-form
        if self.Meta.resource_name == 'datapointentry':
            return super(ModelResource, self).get_list(request, **kwargs)

        if len(objects) > 0:
            # find json_fields ( should be explicit here and check data type)
            # of the field, but for this works..
            json_obj_keys = [k for k, v in objects[0].items() if 'json' in k]

        for obj in objects:

            # serialize json fields ##
            for json_key in json_obj_keys:
                obj[json_key] = json.loads(obj[json_key])

            # hack lvl attribute
            if 'location_type_id' in obj:
                obj['lvl'] = obj['location_type_id'] - 1

            bundles.append(obj)

        response_meta = self.get_response_meta(len(objects))

        response_data = {
            'objects': bundles,
            'meta': response_meta,  # add paginator info here..
            'error': None,
        }

        return self.create_response(request, response_data)

    def get_response_meta(self, object_len):

        meta_dict = {
            'top_lvl_location_id': self.top_lvl_location_id,
            'limit': None,  # paginator.get_limit(),
            'offset': None,  # paginator.get_offset(),
            'total_count': object_len,
        }
        return meta_dict

class BaseNonModelResource(Resource):
    '''
    NOTE: This applies to only the V1 API.  This is only used for the
    /api/v1/datapoint endpoint.

    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta:
        authentication = MultiAuthentication(CustomSessionAuthentication(), ApiKeyAuthentication())
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        always_return_data = True
        cache = CustomCache()
        serializer = CustomSerializer()

    def dehydrate(self, bundle):
        bundle.data.pop("resource_uri", None)
        return bundle

def get_locations_to_return_from_url(request):
    '''
    This method is used in both the /geo and /datapoint endpoints.  Based
    on the values parsed from the URL parameters find the locations needed
    to fulfill the request based on the four rules below.
    1  region__in returns geo data for the regions requested
    2. passing only parent_region__in  should return the shapes for all the
       immediate children in that region if no level parameter is supplied
    3. no params - return locations that the user can see.

    TO DO - Move all advanced logic from location resource here.

    '''
    try:
        location_id__in = request.GET['location_id__in']
    except KeyError:
        location_id__in = []

    top_lvl_location_id = LocationPermission.objects\
        .get(user_id=request.user.id).top_lvl_location_id

    location_id__in.append(top_lvl_location_id)
    location_ids = LocationTree.objects\
        .filter(parent_location_id__in = location_id__in)\
        .values_list('location_id',flat=True)
        
    return location_ids


def html_decorator(func):
    """
    This decorator wraps the output of the django debug tooldbar in html.
    (From http://stackoverflow.com/a/14647943)
    """

    def _decorated(*args, **kwargs):
        response = func(*args, **kwargs)

        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")

        return HttpResponse(wrapped)

    return _decorated

@html_decorator
def api_debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("api_debug/", "")

    view = urlresolvers.resolve(api_url)

    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept

    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)
