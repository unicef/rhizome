import json
import pprint as pp
import traceback
from collections import defaultdict
from datetime import datetime
from itertools import product
from math import isnan

from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ALL, ModelResource, Resource
from tastypie.validation import Validation
from pandas import DataFrame
from pandas import concat, merge, unique, pivot_table
from django.db.models import Sum
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from datapoints.models import *
from datapoints.api.meta_data import *
from datapoints.api.serialize import CustomSerializer

class ResultObject(object):
    '''
    This is the same as a row in the CSV export in which one row has a distinct
    region / campaign combination, and the remaing columns represent the
    indicators requested.  Indicators are a list of IndicatorObjects.
    '''
    region = None
    campaign = None
    indicators = list()

class DataPointResource(BaseNonModelResource):
    '''
    '''

    error = None
    parsed_params = {}
    region = fields.IntegerField(attribute = 'region')
    campaign = fields.IntegerField(attribute = 'campaign')
    indicators = fields.ListField(attribute = 'indicators')

    class Meta(BaseNonModelResource.Meta):

        object_class = ResultObject # use the class above to devine the response
        resource_name = 'datapoint' # cooresponds to the URL of the resource
        max_limit = None # return all rows by default ( limit defaults to 20 )
        # serializer = CustomSerializer

    def get_object_list(self,request):
        '''
        '''

        self.error = None
        results = []

        err = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return []

        err, region_ids = self.get_regions_to_return_from_url(request)
        if err:
            self.error = err
            return []

        print '====\n' * 5
        print region_ids

        db_data = DataPointAbstracted.objects.filter(
            region_id__in = region_ids,
            campaign_id__in = self.parsed_params['campaign__in'])

        for row in db_data:
            r = ResultObject()
            r.region = row.region_id
            r.campaign = row.campaign_id

            indicator_json = row.indicator_json
            cleaned = self.clean_indicator_json(indicator_json)

            r.indicators = cleaned

            results.append(r)


        return results

    def clean_indicator_json(self,indicator_json):

        cleaned = []

        for k,v in indicator_json.iteritems():

            if int(k) in self.parsed_params['indicator__in']:

                indicator_dict = {'indicator':k,'value':v}
                cleaned.append(indicator_dict)

        return cleaned


    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional build_agg_rc_dfing may be applied
        '''

        return self.get_object_list(bundle.request)

    def obj_get(self):
        # get one object from data source
        pk = int(kwargs['pk'])
        try:
            return data[pk]
        except KeyError:
            raise NotFound("Object not found")


    def alter_list_data_to_serialize(self, request, data):
        '''
        If there is an error for this resource, add that to the response.  If
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well
        '''

        ## get rid of the meta_dict. i will add my own meta data.
        data['meta'].pop("limit",None)

        ## iterate over parsed_params
        meta_dict = {}
        for k,v in self.parsed_params.iteritems():
            meta_dict[k] = v

        ## add metadata to response
        data['meta'] = meta_dict

        ## add errors if it exists
        if self.error:
            data['error'] = self.error
        else:
            data['error'] = None


        return data

    def dehydrate(self, bundle):
        '''
        This method allws me to remove or add information to each data object,
        for instance the resource_uri.
        '''

        bundle.data.pop('resource_uri')

        return bundle


    ##########################
    ##### HELPER METHODS #####
    ##########################


    def parse_url_params(self,query_dict):
        '''
        For the query dict return another dictionary ( or error ) in accordance
        to the expected ( both required and optional ) parameters in the request
        URL.
        '''

        parsed_params = {}

        ## try to find optional parameters in the dictionary. If they are not
        ## there return the default values ( given in the dict below)
        optional_params = {'the_limit':10000,'the_offset':0,'agg_level':'mixed',\
            'campaign_start':'2012-01-01','campaign_end':'2900-01-01' ,\
            'campaign__in':None,'region__in': None}

        for k,v in optional_params.iteritems():
            try:
                parsed_params[k] = query_dict[k]
            except KeyError:
                parsed_params[k] = v

        ## find the Required Parameters and if they
        ## dont exists return an error to the response
        required_params = {'indicator__in': None}

        for k,v in required_params.iteritems():

            try:
                parsed_params[k] = [ int(p) for p in  query_dict[k].split(',') ]
            except KeyError as err:
                err_msg = '%s is a required parameter!' % err
                return err_msg , None


        campaign_in_param = parsed_params['campaign__in']

        if campaign_in_param:
            campaign_ids = campaign_in_param.split(',')

        else:
            campaign_ids = self.get_campaign_list(
                parsed_params['campaign_start'],parsed_params['campaign_end']
            )

        parsed_params['campaign__in'] = campaign_ids

        self.parsed_params = parsed_params

        return None


    def get_campaign_list(self,campaign_start,campaign_end):
        '''
        Based on the parameters passed for campaigns, start/end or __in
        return to the parsed params dictionary a list of campaigns to query
        '''

        cs = Campaign.objects.filter(
            start_date__gte = campaign_start,\
            start_date__lte = campaign_end,\
        )

        campaign__in = [c.id for c in cs]

        return campaign__in


class DataPointEntryResource(ModelResource):

    # for validation
    required_keys = [
        'datapoint_id', 'indicator_id', 'region_id',
        'campaign_id', 'value', 'changed_by_id',
    ]
    # for validating foreign keys
    keys_models = {
        'region_id': Region,
        'campaign_id': Campaign,
        'indicator_id': Indicator
    }
    region = fields.IntegerField(attribute = 'region_id')
    campaign = fields.IntegerField(attribute = 'campaign_id')
    indicator = fields.IntegerField(attribute = 'indicator_id')


    class Meta():
        queryset = DataPoint.objects.all()
        # authentication = ApiKeyAuthentication() # sup w this
        authorization = Authorization()
        allowed_methods = ['get'] # TODO FIXME: once obj_create is fully tested, add POST etc
        resource_name = 'datapointentry'
        always_return_data = True
        max_limit = None # no pagination
        filtering = {
            'indicator': ALL,
            'campaign': ALL,
            'region': ALL,
        }


    def obj_create(self, bundle, **kwargs):
        """
        Make sure the data is valid, then save it.
        """
        try:
            self.validate_object(bundle.data)

            existing_datapoint = self.get_existing_datapoint(bundle.data)
            if existing_datapoint is not None:
                update_kwargs = {
                    'region_id': existing_datapoint.region_id,
                    'campaign_id': existing_datapoint.campaign_id,
                    'indicator_id': existing_datapoint.indicator_id
                }
                bundle.response = self.success_response()
                return super(DataPointEntryResource, self).obj_update(bundle, **update_kwargs)
            else:
                bundle.response = self.success_response()
                return super(DataPointEntryResource, self).obj_create(bundle, **kwargs)

        except InputError, e:
            bundle.data = self.make_error_response(e)
            response = self.create_response(bundle.request, bundle)
            raise ImmediateHttpResponse(response=response)

        # catch all exceptions & format them the way the client is expecting
        except Exception, e:
            e.code = 0
            e.data = traceback.format_exc()
            print e.data
            bundle.data = self.make_error_response(e)
            response = self.create_response(bundle.request, bundle)
            raise ImmediateHttpResponse(response=response)

    def get_existing_datapoint(self, data):
        """
        Assumes data is valid
        (i.e. data should have passed validate_object first)
        """
        try:
            obj = DataPoint.objects.get(region_id=int(data['region_id']),
                campaign_id=int(data['campaign_id']),
                indicator_id=int(data['indicator_id']),
            )
            return obj
        except ObjectDoesNotExist:
            return

    def hydrate(self, bundle):

        if hasattr(bundle, 'obj') and isinstance(bundle.obj, DataPoint) \
            and hasattr(bundle.obj, 'region_id') and bundle.obj.region_id is not None \
            and hasattr(bundle.obj, 'campaign_id') and bundle.obj.region_id is not None \
            and hasattr(bundle.obj, 'indicator_id') and bundle.obj.region_id is not None:
            pass
        else:
            bundle.obj = DataPoint()

            bundle.obj.source_datapoint_id = int(bundle.data['datapoint_id'])
            bundle.obj.region_id = int(bundle.data['region_id'])
            bundle.obj.campaign_id = int(bundle.data['campaign_id'])
            bundle.obj.indicator_id = int(bundle.data['indicator_id'])
            bundle.obj.changed_by_id = int(bundle.data['changed_by_id'])
            bundle.obj.value = bundle.data['value']

        return bundle

    def dehydrate(self, bundle):
        # hack: bundle will only have a response attr if this is a POST or PUT request
        if hasattr(bundle, 'response'):
            bundle.data = bundle.response
        else: # otherwise, this is a GET request
            bundle.data['datapoint_id'] = bundle.data['id']
            del bundle.data['id']
            for key in ['campaign', 'indicator', 'region']:
                bundle.data['{0}_id'.format(key)] = bundle.data[key]
                del bundle.data[key]
            for key in ['created_at', 'resource_uri']:
                del bundle.data[key]
        return bundle

    def validate_object(self, obj):
        """
        Check that object has all the right fields, yadda yadda yadda.
        """
        for key in self.required_keys:
            if not key in obj:
                raise InputError(2, 'Required metadata missing: {0}'.format(key))

        # ensure that metadata values are valid
        for key, model in self.keys_models.iteritems():
            try:
                key_id = int(obj[key])
            except ValueError:
                raise InputError(4, 'Invalid metadata value: {0}'.format(key))
            try:
                instance = model.objects.get(id=key_id)
            except (ValueError, ObjectDoesNotExist):
                raise InputError(3, 'Could not find record for metadata value: {0}'.format(key))

    def validate_object_update(self, obj):
        """
        When updating an object, validate the new data.
        """
        # what should we do about id, url, created_at ?
        # those all get filled in automatically, right?

        # should this be a required key? yeah
        assert obj.has_key('changed_by_id')
        user_id = int(obj['changed_by_id'])
        User.objects.get(id=user_id)

        # ensure that region, campaign, and indicator, if present, are valid values
        if obj.has_key('region_id'):
            region_id = int(obj['region_id'])
            Region.objects.get(id=region_id)

        if obj.has_key('campaign_id'):
            campaign_id = int(obj['campaign_id'])
            Campaign.objects.get(id=campaign_id)

        if obj.has_key('indicator_id'):
            indicator_id = int(obj['indicator_id'])
            Indicator.objects.get(id=indicator_id)

    def success_response(self):
        response = {
            'success': 1
        }
        return response

    def make_error_response(self, error):
        response = {
            'success': 0,
            'error': {
                'code': error.code,
                'message': error.message
            }
        }
        if hasattr(error, 'data'):
            response['error']['data'] = error.data
        return response


class InputError(Exception):

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        if data is not None:
            self.data = data
