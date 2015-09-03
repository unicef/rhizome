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
    permissions are appled for GET and POST for the datapoint resource
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
        Overriden from Tastypie..
        """

        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        paginator = self._meta.paginator_class(request.GET, sorted_objects, resource_uri=self.get_resource_uri(), limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [obj for obj in to_be_serialized[self._meta.collection_name]]

        response_data = {
            'objects': bundles,
            'meta': [],
            'error': None
        }

        return self.create_response(request, response_data)

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

    def parse_url_strings(self,query_dict):
        '''
        As the geo endpoint is based off of the region/parent_region paremeter
        we go through a pretty hacky try / except frenzy in order to find the
        parameters necessary to get region/shape data for the front end.  The
        parameters here for region_in,level, and parent_region in were
        constructed in accordance to the request from the front end team.
        '''

        self.region__in, self.region_type_id, self.parent_region__in = \
            None, None, None

        ## REGION_ID
        try:
            self.region__in = [int(r) for r in query_dict['region__in']\
                .split(',')]
        except KeyError:
            pass
        except ValueError:
            pass

        ## REGION TYPE ##
        try:
            self.region_type_id = RegionType.objects.get(name = query_dict\
                ['level'].lower()).id
        except KeyError:
            pass
        except ObjectDoesNotExist:
            all_r_types = RegionType.objects.all().values_list('name',flat=True)
            err = 'region type doesnt exist. options are:  %s' % all_r_types
            return err, []

        try:
            self.parent_region__in = [int(r) for r in query_dict['parent_region__in']\
                .split(',')]
        except KeyError:
            pass
        except ValueError:
            pass

        return None


    def get_regions_to_return_from_url(self,request):
        '''
        This method is used in both the /geo and /datapoint endpoints.  Based
        on the values parsed from the URL parameters find the regions needed
        to fulfill the request based on the four rules below.
        1  region__in returns geo data for the regions requested
        2. passing only parent_region__in  should return the shapes for all the
           immediate children in that region if no level parameter is supplied
        3. no params - return regions at the top of the tree ( no parent_id).
        After the four steps are worked through in this method, we apply the
        permissions function in order to determine the final list of regions
        to return based on the user making the request.
        '''

        ## attach these to self and return only error #
        err = self.parse_url_strings(request.GET)

        if err:
            self.err = err
            return err, []

        ## CASE 1 ##
        if self.region__in is not None:

            region_ids = Region.objects.filter(id__in = self.region__in)\
                .values_list('id',flat=True)

        ## CASE 2 #
        elif self.parent_region__in is not None and self.region_type_id is None:

            region_ids = Region.objects.filter(parent_region__in = \
                self.parent_region__in).values_list('id',flat=True)

        else:
            region_ids = Region.objects.filter(parent_region_id__isnull=True).\
                values_list('id',flat=True)

        ## now apply regional permissions ##

        # permitted_region_qs = RegionTree.objects.filter(parent_region_id__in =\
        #     region_ids).values_list('region_id',flat=True)

        # final_region_ids = list(set(region_ids).intersection(set\
        #     (permitted_region_ids)))

        return None, region_ids
