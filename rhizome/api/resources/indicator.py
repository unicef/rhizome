import json

from django.http import HttpResponse

from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.utils import is_valid_jsonp_callback_value, dict_strip_unicode_keys

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import Indicator

class IndicatorResource(BaseModelResource):
    '''
    **GET Request** Returns all indicators
        - *Optional Parameters:* 
            'id': return only the id(s) specified
        - *Errors:*
            If an error occurs, the API returns 200 code and an empty list of indicators
    
    **POST Request** Creates an indicator
        - *Required Parameters:* 
            'name, 'short_name', 'description','good_bound', 'bad_bound', 'source_name'
        - *Optional Parameters:* 
            'id', 'data_format' (defaults to int)
        - *Errors:* 
            if any of the required fields are missing or incorrect, the API returns a 500 error code.
    '''

    class Meta(BaseModelResource.Meta):
        resource_name = 'indicator'
        filtering = {
            "id": ALL,
        }

    def get_object_list(self, request):

        indicator_id_list = []

        try:
            indicator_id = int(request.GET['id'])
            indicator_id_list.append(indicator_id)
        except KeyError:
            pass

        try:
            indicator_id_list = [int(x) for x in request.GET['id__in'].split(',')]
        except KeyError:
            pass

        if len(indicator_id_list) == 0:
            return Indicator.objects.all().values()

        else:
            return Indicator.objects.filter(id__in=indicator_id_list).values()


    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def obj_create(self, bundle, **kwargs):

        post_data = bundle.data

        try:
            ind_id = int(post_data['id'])
            if ind_id == -1:
                ind_id = None
        except KeyError:
            ind_id = None

        try:
            data_format = post_data['data_format']
        except KeyError:
            data_format = 'int'

        try:
            defaults = {
                'name': post_data['name'],
                'short_name': post_data['short_name'],
                'description': post_data['description'],
                'data_format': data_format,
                'good_bound': post_data['good_bound'],
                'bad_bound': post_data['bad_bound'],
                'source_name': post_data['source_name']
            }
        except Exception as error:
            data = {
                'error': 'Please provide ' + str(error) + ' for the indicator.',
                'code': -1
            }
            raise ImmediateHttpResponse(response=HttpResponse(json.dumps(data),
                                        status=500,
                                        content_type='application/json'))

        try:
            ind, created = Indicator.objects.update_or_create(
                id=ind_id,
                defaults=defaults
            )
        except Exception as error:
            data = {
                'error': error.message,
                'code': -1
            }
            raise ImmediateHttpResponse(response=HttpResponse(json.dumps(data),
                                        status=422,
                                        content_type='application/json'))

        bundle.obj = ind
        bundle.data['id'] = ind.id

        return bundle
