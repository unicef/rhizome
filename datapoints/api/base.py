from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource, Resource, ALL

from datapoints.models import RegionType,Region

class BaseModelResource(ModelResource):
    '''
    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta():
        # authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        allowed_methods = ['get','post','put','patch', 'delete']
        filtering = {
            "id": ALL,
        }

class BaseNonModelResource(Resource):
    '''
    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta():
        # authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True

    def parse_url_strings(self,query_dict):

        self.region__in, self.region_type_id, self.parent_region__in = \
            None, None, None

        ## REGION_ID
        try:
            self.region__in = [int(r) for r in query_dict['region__in']\
                .split(',')]
        except KeyError:
            pass

        ## REGION TYPE ##
        try:

            self.region_type_id = RegionType.objects.get(name = query_dict\
                ['region_type']).id

        except KeyError:
            pass

        except ObjectDoesNotExist:

            all_r_types = RegionType.objects.all().values_list('name',flat=True)

            err = 'region type doesnt exist. options are' + str(all_r_types)

            return err, []


        try:
            self.parent_region__in = [int(r) for r in query_dict['parent_region__in']\
                .split(',')]
        except KeyError:
            pass

        return None


    def get_regions_to_return_from_url(self,request):
        '''
        1  region__in returns geo data for the regions requested
        2. parent_region__in + level should return the shapes for all the child
           regions at the specified level that are within the region specified
        3. passing only parent_region__in  should return the shapes for all the
           immediate children in that region if no level parameter is supplied
        4. no params - return top 10 regions
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
        elif self.parent_region__in is not None and self.region_type_id is not None:

            region_ids = RegionHeirarchy.objects.filter(
                contained_by_region_id__in = self.parent_region__in, \
                region_type_id = self.region_type_id)\
                .values_list('region_id',flat=True)

        ## CASE 3 #
        elif self.parent_region__in is not None and self.region_type_id is None:

            region_ids = Region.objects.filter(parent_region__in = \
                self.parent_region__in)

        else:
            region_ids = Region.objects.all().values_list('id',flat=True)[:5]


        return None, region_ids



def html_decorator(func):
    """
    This decorator wraps the output in html.
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
