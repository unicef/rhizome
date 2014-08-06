from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from django.core.exceptions import ObjectDoesNotExist

from datapoints.models import *



def parse_slugs_from_url(query_dict):
    ''' given the query dictionary passed from the get request parse the \
    slug and find the ID'''

    indicator_id = get_id_from_slug_param('indicator_slug', \
        query_dict,Indicator)

    region_id = get_id_from_slug_param('region_slug', \
        query_dict,Region)

    campaign_id = get_id_from_slug_param('campaign_slug', \
        query_dict,Campaign)

    indicator_part_id = get_id_from_slug_param('indicator_part', \
        query_dict,Indicator)

    indicator_whole_id = get_id_from_slug_param('indicator_whole', \
        query_dict,Indicator)

    # return indicator_id, region_id

    return indicator_id, region_id, campaign_id, indicator_part_id \
        ,indicator_whole_id

def get_id_from_slug_param(slug_key,query_dict,model):

    try:
        slug = query_dict[slug_key]
        obj_id = model.objects.get(slug=slug).id
    except KeyError:
        obj_id = None
        # there was an no indicator_slug in request
    except ObjectDoesNotExist:
        obj_id = None

    return obj_id
