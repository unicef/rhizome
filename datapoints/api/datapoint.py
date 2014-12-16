import pprint as pp
from math import isnan
from collections import defaultdict
from itertools import product

from tastypie.serializers import Serializer
from tastypie.resources import ALL
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.resources import Resource
from pandas import DataFrame
from pandas import concat, merge, unique
from django.db.models import Sum
from django.db import connection

from datapoints.models import *
from datapoints.api.meta_data import *



class CustomSerializer(Serializer):
    formats = ['json', 'csv']
    content_types = {
        'json': 'application/json',
        'csv': 'text/csv',
    }


    def to_csv(self, data, options=None):

        options = options or {}
        data = self.to_simple(data, options)

        # print DataFrame(data['objects'])

        # csv = StringIO.StringIO(str(pivoted.to_csv()))

        # return csv
        return data

class ResultObject(object):
    '''
    This is the same as a row in the CSV export in which one row has a distinct
    region / campaign combination, and the remaing columns represent the
    indicators requested.  Indicators are a list of IndicatorObjects.
    '''
    region = None
    campaign = None
    indicators = list()


class DataPointResource(Resource):
    '''
    This Resource is custom and builds upon the tastypie Model Resource by
    overriding the methods coorsponding to GET requests.  For more information
    on creating custom api functionality see :
      https://gist.github.com/nomadjourney/794424
      http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
    '''

    error = None
    parsed_params = {}
    region = fields.IntegerField(attribute = 'region')
    campaign = fields.IntegerField(attribute = 'campaign')
    indicators = fields.ListField(attribute = 'indicators')


    class Meta(BaseApiResource.Meta):

        object_class = ResultObject # use the class above to devine the response
        resource_name = 'datapoint' # cooresponds to the URL of the resource
        max_limit = None # return all rows by default ( limit defaults to 20 )
        serializer = CustomSerializer()


    def get_object_list(self,request):
        '''
        This method is overriden from tastypie.  When using a model resource
        the typical behavior of this method woudl be to select all datapoints
        for example.  Instead, all of this behaviour is 100pct custom and
        and cooresponds to the business case that we need to accomidate
        as well as the requirements of the front end application.
        '''

        err,parsed_params = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return []

        ## find the distinct regions/campaigns and slice by limit/offset
        err, r_c_df = self.build_campaign_region_df(parsed_params)

        if err:
            self.error = err
            return []

        indicators = [int(ind) for ind in parsed_params['indicator__in']]

        campaigns,regions = list(r_c_df.campaign.apply(int).unique()), \
            list(r_c_df.region.apply(int).unique())

        dp_df = self.build_stored_df(campaigns,indicators,regions)
        aggregated_dp_df = self.build_aggregate_df(campaigns,indicators,regions)


        dp_df['is_agg'] = 0
        aggregated_dp_df['is_agg'] = 1

        final_df = concat([dp_df,aggregated_dp_df])

        results = self.dp_df_to_list_of_results(final_df)


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


    def build_campaign_region_df(self,parsed_params):
        '''
        Build a dataframe that represents the regions and campaigns relevant to
        the request.  These tuples fit the offset / limit bounds.  This method
        does not check if there is data for the region/campaign combo for the
        indicator(s) provided, because for queries in which the region
        does not have the data we will need to aggregate by the parents children

        I also need to make sure that i filter out the records here that dont
        have any data at all, but NOT records for which their children have data.
        That means that i build two DFs, one for which there is data stored,
        and another for which there is data stored for its children ( with
        the indicator and campaign stored as well)
        '''

        shared_df_cols = ['campaign','indicator','region']

        # regions, campaigns, indicators, the_offset, the_limit =
        campaigns, indicators, regions, the_offset, the_limit = parsed_params['campaign__in'],\
            parsed_params['indicator__in'],\
            parsed_params['region__in'],\
            int(parsed_params['the_offset']), \
            int(parsed_params['the_limit'])

        df_w_data = DataFrame(list(DataPoint.objects.filter(
            campaign__in = campaigns,\
            indicator__in = indicators,\
            region__in = regions).values_list(\
            'campaign','indicator','region').distinct()),columns=shared_df_cols)

        parent_region_lookup = []
        all_children = []

        for r in regions:

            r_obj = Region.objects.get(id=r)

            for chld in r_obj.get_all_children():
                parent_region_lookup.append([chld.id,r])
                all_children.append(chld.id) ## this is kinda lame

        children_regions_with_data_df = DataFrame(list(DataPoint.objects.filter(
            campaign__in = campaigns,\
            indicator__in = indicators,\
            region__in = set(all_children)).values_list(\
            'campaign','indicator','region').distinct()),columns= \
                ['campaign','indicator','child_region'])


        region_lookup_df = DataFrame(parent_region_lookup,columns=\
            ['child_region','region'])

        parent_lookup_df = merge(children_regions_with_data_df,region_lookup_df,\
            on='child_region')

        # parent_lookup_df.drop('child_region')
        de_duped_agg_df = parent_lookup_df.drop_duplicates(subset = shared_df_cols)


        print 'LEN DATA DF \n' * 10

        print len(df_w_data)
        unioned_df = concat([df_w_data,de_duped_agg_df])

        ## slice the unioned DF with the offset / limit provided
        offset_df = unioned_df[the_offset:the_limit + the_offset]

        if len(df_w_data) <= the_offset:
            err = 'the offset must be less than the total number of objects!'
            return err, None

        # will save this to the meta object to allow for pagination
        self.parsed_params['total_count'] = len(unioned_df)
        self.parsed_params['total_count_agg'] = len(de_duped_agg_df)
        self.parsed_params['total_count_no_agg'] = len(df_w_data)

        return None, offset_df



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
                parsed_params[k] = [ int(p) for p in  query_dict[k].split(',') ]
            except KeyError as err:
                err_msg = str(err).replace('"','') + ' is a required paramater!'
                return err_msg , None


        self.parsed_params = parsed_params

        return None, parsed_params


    def find_campaigns(self,query_dict):
        '''
        Based on the parameters passed for campaigns, start/end or __in
        return to the parsed params dictionary a list of campaigns to query
        '''
        try:
            ## if the campaign_in parameter exists return this
            ## and ignore the campaign_start and end parameters.
            campaign__in = [int(c) for c in query_dict['campaign__in'].split(',')]
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


    def dp_df_to_list_of_results(self,dp_df):

        results = []

        re_indexed_df = dp_df.set_index(['region_id','campaign_id'])

        # key: tuple (region/campaign) value: list of dicts
        results_dict = defaultdict(list)

        for rc_tuple, indicators in re_indexed_df.iterrows():
            indicator_dict = {}
            indicator_dict['indicator'] = indicators.indicator_id
            indicator_dict['value'] = indicators.value
            indicator_dict['datapoint_id'] = indicators.id
            indicator_dict['is_agg'] = indicators.is_agg

            results_dict[rc_tuple].append(indicator_dict)

        for rc_tuple, indicator_list_of_dicts in results_dict.iteritems():
            new_obj = ResultObject()
            new_obj.region = rc_tuple[0]
            new_obj.campaign = rc_tuple[1]
            new_obj.indicators = indicator_list_of_dicts

            results.append(new_obj)

        return results


    def build_stored_df(self,campaigns,indicators,regions):

        ## find data for the requested regions campaigns and indicators
        ## get datapoints according to regions/campaigns/indicators ##
        dp_columns = ['id','indicator_id','campaign_id','region_id','value']

        try:
            dp_df = DataFrame(list(DataPoint.objects.filter(
                region__in = regions,\
                campaign__in = campaigns,\
                indicator__in = indicators).values()))[dp_columns]
        except KeyError:
            dp_df = DataFrame(columns=dp_columns)

        return dp_df


    def build_aggregate_df(self,campaigns,indicators,regions):
        '''
        Taking the keys that are missing data.. find the child regions
        and query the datapoints table, returning the aggregate value for
        each parent region, indicator, campaign combo.

        I would really like to be explicit about the c,i,r thing tuple set.
        I'm usign the convention for alphabetical order, but i want to make this
        explicit with either a dictionary or dataframe.
        '''

        ## we should get back one row for each of the tuples below
        expected_data = set(product(campaigns,indicators,regions))

        ## this is the data that exists for the keys given
        key_combos_with_data = set(DataPoint.objects.filter(
            indicator__in = indicators,\
            region__in = regions,\
            campaign__in = campaigns).values_list(\
                'campaign','indicator','region').distinct())

        key_combos_missing_data = expected_data.difference(key_combos_with_data)


        ## TO DO - dont use an iterator here, but make one query to the regions
        ## /datapoints table, group by parent region id and return that
        ## as your dataframe

        all_dps = []

        for c,i,r in key_combos_missing_data:

            parent_region = Region.objects.get(id=r)
            child_regions = parent_region.get_all_children()

            sum_of_child_regions = DataPoint.objects.filter(
                    campaign_id = c,\
                    indicator_id = i ,\
                    region__in=child_regions).aggregate(Sum('value'))

            cir = {}
            cir ['campaign_id'] = c
            cir ['indicator_id'] = i
            cir ['region_id'] = r
            cir['value'] = sum_of_child_regions['value__sum']
            cir['id'] = -1

            if sum_of_child_regions['value__sum']:
                all_dps.append(cir)


        return DataFrame(all_dps)
