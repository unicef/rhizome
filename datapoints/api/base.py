from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import Authentication
from tastypie.resources import ModelResource, Resource, ALL

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


class BaseModelResource(ModelResource):
    '''
    NOTE: This applies to only the V1 API.  This method inherits from Tastypie's
    model resource.  Each specific model resource in the V1 Api inherits this
    class.

    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta():
        authentication = CustomAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        allowed_methods = ['get','post','put','patch', 'delete']
        filtering = {
            "id": ALL,
        }

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
        2. parent_region__in + level should return the shapes for all the child
           regions at the specified level that are within the region specified
        3. passing only parent_region__in  should return the shapes for all the
           immediate children in that region if no level parameter is supplied
        4. no params - return top 10 regions.

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


        ## CASE 2 ##
        # elif self.parent_region__in is not None and self.region_type_id is not None:
        #     ## FIX ME - use fn_get_authorized_regions_by_user() instead
        #
        #     region_ids = RegionHeirarchy.objects.filter(
        #         contained_by_region_id__in = self.parent_region__in, \
        #         region_type_id = self.region_type_id)\
        #         .values_list('region_id',flat=True)
        #
        #     if len(region_ids) == 0:
        #
        #         err = 'no regions of region_type_id: %s exists under region_id\
        #             %s ' % (self.region_type_id, self.parent_region__in)
        #
        #         return err, region_ids

        ## CASE 3 #
        elif self.parent_region__in is not None and self.region_type_id is None:

            region_ids = Region.objects.filter(parent_region__in = \
                self.parent_region__in).values_list('id',flat=True)

        else:
            region_ids = Region.objects.all().values_list('id',flat=True)

        ####################################
        ## now apply regional permissions ##
        ####################################

        permitted_region_qs =  Region.objects.raw("SELECT * FROM\
            fn_get_authorized_regions_by_user(%s,%s,'r',NULL)",\
            [self.user_id,list(region_ids)])

        permitted_region_ids = [r.id for r in permitted_region_qs]

        final_region_ids = list(set(region_ids).intersection(set\
            (permitted_region_ids)))

        return None, final_region_ids


    def get_list(self, request, **kwargs):
        '''
        Overriding this just so i can access the user_id attribute within the
        resource.
        '''

        self.user_id = request.user.id
        args = []

        return super(BaseNonModelResource, self).get_list(request, **kwargs)

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
def debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("debug/", "")

    view = urlresolvers.resolve(api_url)

    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept

    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)
