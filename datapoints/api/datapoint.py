from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.resources import Resource
from pandas import DataFrame

from datapoints.models import *
from datapoints.api.meta_data import *



class ResultObject(object):
    '''
    This is the same as a row in the CSV export in which one row has a distinct
    region / campaign combination, and the remaing columns represent the
    indicators requested.  Indicators are a list of IndicatorObjects.
    '''

    pk = None
    # campaign = None
    # region = None
    # changed_by_id = None
    # indicators = []


class IndicatorObject(object):
    '''
    This object represents the indicators and values for the region/campaign
    combinations.  Within each Result Object, there are N Inidcator objects
    with the attributes listed below.
    '''
    indicator = None
    value = None
    is_agg = None


class DataPointResource(Resource):
    '''
    This Resource is custom and builds upon the tastypie Model Resource by
    overriding the methods coorsponding to GET requests.  For more information
    on creating custom api functionality see :
      https://gist.github.com/nomadjourney/794424
      http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
    '''
    error = None
    pk = fields.IntegerField(attribute = 'id')

    # region = fields.ToOneField(RegionResource, 'region')
    # indicator = fields.ToOneField(IndicatorResource, 'indicator')
    # campaign = fields.ToOneField(CampaignResource, 'campaign')
    # changed_by_id = fields.ToOneField(UserResource, 'changed_by')


    class Meta(BaseApiResource.Meta):
        object_class = ResultObject
        resource_name = 'datapoint'
        max_limit = None
        # serializer = CustomSerializer()


    def detail_uri_kwargs(self, bundle_or_obj):
            kwargs = {}

            if isinstance(bundle_or_obj, Bundle):
                kwargs['pk'] = bundle_or_obj.obj.pk
            else:
                kwargs['pk'] = bundle_or_obj.pk

            return kwargs

    def get_object_list(self,request):

        results = []

        err,params = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return results


        ## get distinct regions/campaigns for the provided indicators
        all_region_campaign_tuples = DataPoint.objects.filter(indicator__in=\
            params['indicator__in']).values_list('region','campaign').distinct()

        df = DataFrame(list(all_region_campaign_tuples),columns=['region',\
            'campaign'])

        print df

        for result in range(0,5):

            new_obj = ResultObject()
            new_obj.id = result
            results.append(new_obj)

        return results


    def obj_get_list(self,bundle,**kwargs):
        '''
        Outer method for get_object_list... this calls get_object_list and
        could be a point at which additional filtering may be applied
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
        there is no error, than add this key, but set the value to null'''

        if self.error:
            data['error'] = self.error
        else:
            data['error'] = None

        return data


    ##########################
    ##### HELPER METHODS #####
    ##########################

    def parse_url_params(self,query_dict):

        parsed_params = {}

        optional_params = {
            'region__in':None,'campaign__in':None,'campaign_end':None,\
            'campaign_start':None,'the_limit':None,'the_offset':0,
            'uri_format':'id','agg_level':'mixed'}

        required_params = {'indicator__in':None}


        for k,v in required_params.iteritems():

            try:
                parsed_params[k] = query_dict[k].split(',')
            except KeyError as err:
                return str(err).replace('"','') + ' is a required paramater!', None

        return None, parsed_params
