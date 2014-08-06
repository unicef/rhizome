from tastypie.resources import ModelResource,Resource, ALL
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization

from django.core.exceptions import ObjectDoesNotExist

from datapoints.models import *


class BaseApiResource(Resource):
    '''
    This is the top level class all other Resource Classes inherit from this.
    The API Key authentication is defined here and thus is required by all
    other resources.  This class enherits fro the Tastyppie "ModelResource"

    See Here: http://django-tastypie.readthedocs.org/en/latest/resources.html?highlight=modelresource
    '''

    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True


    def parse_slugs_from_url(self,query_dict):
        ''' given the query dictionary passed from the get request parse the \
        slug and find the ID'''

        indicator_id = self.get_id_from_slug_param('indicator_slug', \
            query_dict,Indicator)

        region_id = self.get_id_from_slug_param('region_slug', \
            query_dict,Region)

        campaign_id = self.get_id_from_slug_param('campaign_slug', \
            query_dict,Campaign)

        indicator_part_id = self.get_id_from_slug_param('indicator_part', \
            query_dict,Indicator)

        indicator_whole_id = self.get_id_from_slug_param('indicator_whole', \
            query_dict,Indicator)

        api_method_id = self.get_id_from_slug_param('api_method', \
            query_dict,Indicator)


        return indicator_id, region_id, campaign_id, indicator_part_id \
            ,indicator_whole_id

    def get_id_from_slug_param(self,slug_key,query_dict,model):

        try:
            slug = query_dict[slug_key]
            obj_id = model.objects.get(slug=slug).id
        except KeyError:
            obj_id = None
            # there was an no indicator_slug in request
        except ObjectDoesNotExist:
            obj_id = None

        return obj_id
