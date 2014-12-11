import pprint as pp
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

    campaign = None
    region = None
    indicators = dict()


class IndicatorObject(object):
    '''
    This object represents the indicators and values for the region/campaign
    combinations.  Within each Result Object, there are N Inidcator objects
    with the attributes listed below.
    '''
    indicator = None
    value = None
    is_agg = None
    datapoint_id = None



class DataPointResource(Resource):
    '''
    This Resource is custom and builds upon the tastypie Model Resource by
    overriding the methods coorsponding to GET requests.  For more information
    on creating custom api functionality see :
      https://gist.github.com/nomadjourney/794424
      http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
    '''

    error = None
    total_count = 0
    campaign = fields.IntegerField(attribute = 'campaign')
    region = fields.IntegerField(attribute = 'region')
    indicators = fields.Diction


    class Meta(BaseApiResource.Meta):

        object_class = ResultObject # use the class above to devine the response
        resource_name = 'datapoint' # cooresponds to the URL of the resource
        max_limit = None # return all rows by default ( limit defaults to 20 )
        # serializer = CustomSerializer()


    def get_object_list(self,request):
        '''
        This method is overriden from tastypie.  When using a model resource
        the typical behavior of this method woudl be to select all datapoints
        for example.  Instead, all of this behaviour is 100pct custom and
        and cooresponds to the business case that we need to accomidate
        as well as the requirements of the front end application.
        '''

        results = []

        err,parsed_params = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return results

        err, r_c_df = self.build_campaign_region_df(parsed_params)

        if err:
            self.error = err
            return results

        campaigns = list(r_c_df.campaign.unique())
        regions = list(r_c_df.region.unique())
        indicators = parsed_params['indicator__in']

        ## get datapoints according to regions/campaigns/indicators ##
        dp_columns = ['id','indicator_id','campaign_id','region_id','value']
        dp_df = DataFrame(list(DataPoint.objects.filter(
            region__in = regions,\
            campaign__in = campaigns,\
            indicator__in = indicators).values()))[dp_columns]

        re_indexed_df = dp_df.set_index(['region_id','campaign_id'])

        pivoted_dict = re_indexed_df.transpose().to_dict()

        ## pivot the dataframe so that indicators are columns ##

        for rc_tuple, indicator_dict in pivoted_dict.iteritems():

            new_obj = ResultObject()
            new_obj.region = rc_tuple[0]
            new_obj.campaign = rc_tuple[1]
            new_obj.indicators = indicator_dict

            # ind_obj = IndicatorObject()
            #
            # ind_obj.indicator = row_data.indicator_id
            # ind_obj.value = row_data.value
            # ind_obj.is_agg = 0
            # ind_obj.datapoint_id = row_data.id
            #
            # new_obj.indicators = ind_obj
            #
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
        there is no error, than add this key, but set the value to null.  Also
        add the total_count to the meta object as well'''

        data['meta']['total_count'] = self.total_count

        if self.error:
            data['error'] = self.error
        else:
            data['error'] = None



        return data


    ##########################
    ##### HELPER METHODS #####
    ##########################

    def build_campaign_region_df(self,parsed_params):
        '''
        Build a dataframe that represents the regions and campaigns relevant to
        the request.  These tuples fit the offset / limit bounds, as well as the
        region / campaign / indicator filters on the datapoints table.  This way
        we only return region/campaingns that actually have data in the db.
        '''
        ## get distinct regions/campaigns for the provided indicators
        all_region_campaign_tuples = DataPoint.objects.filter(
            indicator__in = parsed_params['indicator__in'],\
            region__in = parsed_params['region__in'],\
            campaign__in = parsed_params['campaign__in']).values_list\
            ('region','campaign').distinct()

        ## will save this to the meta object to allow for pagination
        self.total_count = len(all_region_campaign_tuples)

        ## throw error if the indicators yield no r/c couples
        if len(all_region_campaign_tuples) == 0:
            err = 'There are no datapoints for the parameters requested'
            return err, None


        ## find the offset and the limit
        the_offset, the_limit = int(parsed_params['the_offset']), \
            int(parsed_params['the_limit'])

        ## build a dataframe with the region / campaign tuples and slice it
        ## in accordance to the_offset and the_limit
        df = DataFrame(list(all_region_campaign_tuples),columns=['region',\
            'campaign'])[the_offset:the_limit + the_offset]

        print df
        return None, df



    def parse_url_params(self,query_dict):
        '''
        For the query dict return another dictionary ( or error ) in accordance
        to the expected ( both required and optional ) parameters in the request
        URL.
        '''

        parsed_params = {}

        ## find the campaign__in parameter via the method below
        parsed_params['campaign__in'] = self.find_campaigns(query_dict)

        ## try to find optional parameters in the dictionary. If they are not
        ## there return the default values ( given in the dict below)
        optional_params = {'the_limit':10000,'the_offset':0,
            'uri_format':'id','agg_level':'mixed'}

        for k,v in optional_params.iteritems():
            try:
                parsed_params[k] = query_dict[k]
            except KeyError:
                parsed_params[k] = v

        ## find the Required Parameters and if they
        ## dont exists return an error to the response
        required_params = {'indicator__in': None,'region__in': None}

        for k,v in required_params.iteritems():

            try:
                parsed_params[k] = query_dict[k].split(',')
            except KeyError as err:
                return str(err).replace('"','') + ' is a required paramater!', None

        return None, parsed_params


    def find_campaigns(self,query_dict):
        '''
        Based on the parameters passed for campaigns, start/end or __in
        return to the parsed params dictionary a list of campaigns to query
        '''
        try:
            ## if the campaign_in parameter exists return this
            ## and ignore the campaign_start and end parameters.
            campaign__in = query_dict['campaign__in'].split(',')
            return campaign__in
        except KeyError:
            pass

        try:
            campaign_start = query_dict['campaign_start']
        except KeyError:
            campaign_start = '2001-01-01'

        try:
            campaign_end = query_dict['campaign_end']
        except KeyError:
            campaign_end = '2900-01-01'

        cs = Campaign.objects.filter(
            start_date__gte = campaign_start,\
            start_date__lte = campaign_end,\
        )

        campaign__in = [c.id for c in cs]

        return campaign__in
