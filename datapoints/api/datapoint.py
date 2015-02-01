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

    class Meta(BaseNonModelResource.Meta):

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
        self.error = None

        err,parsed_params = self.parse_url_params(request.GET)

        if err:
            self.error = err
            return []

        ## look up indicators in db.. if ANY of the requested arent in db
        ## throw error to api

        tmp_indicators = [int(ind) for ind in parsed_params['indicator__in']]

        err, indicators = self.check_db_for_indicators(tmp_indicators)

        if err:
            self.error = err
            return []


        ## find the distinct regions/campaigns and slice by limit/offset
        err, r_c_df = self.build_campaign_region_df(parsed_params)

        if err:
            self.error = err
            return []

        campaigns,regions = list(r_c_df.campaign_id.apply(int).unique()), \
            list(r_c_df.region_id.apply(int).unique())

        dp_df = self.build_stored_df(campaigns,indicators,regions)

        ## You should check first to see if you have enough
        ## results to return to the api before you try to aggregate
        ## that is if 5 objects are requested, and there are 6 non aggregated
        ## records of data... dont bother aggregating
        aggregated_dp_df = self.build_aggregate_df(campaigns,indicators,regions)

        dp_df['is_agg'] = 0
        aggregated_dp_df['is_agg'] = 1

        final_df = concat([dp_df,aggregated_dp_df])

        results = self.dp_df_to_list_of_results(final_df,r_c_df,indicators)

        return results


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


    def build_campaign_region_df(self,parsed_params):
        '''
        Build a dataframe that represents the regions and campaigns relevant to
        the request.  These tuples fit the offset / limit bounds.

        I also need to make sure that i filter out the records here that dont
        have any data at all, but NOT records for which their children have data.
        That means that i build two DFs, one for which there is data stored,
        and another for which there is data stored for its children ( with
        the indicator and campaign stored as well)
        '''

        ## find the campaign__in parameter via the method below.. note however
        ## this method only filters on start / end.. not office id.
        err, campaigns = self.filter_campaigns_by_date(parsed_params)

        if err:
            return err, None

        indicators, regions, the_offset, the_limit = parsed_params['indicator__in'],\
            parsed_params['region__in'],\
            int(parsed_params['the_offset']), \
            int(parsed_params['the_limit'])


        try:
            df_w_data = DataFrame(list(AbstractedDataPoint.objects.filter(
                campaign__in = campaigns,\
                indicator__in = indicators,\
                region__in = regions).values_list(\
                'campaign','region').distinct()),columns=['campaign_id','region_id'])

        except ValueError:
            df_w_data = DataFrame(columns= ['campaign_id','region_id'])

        ## get all of the r/c combos that have data ##
        err, de_duped_agg_df = self.build_agg_rc_df(campaigns,indicators,regions)

        if err:
            return err, None


        df_w_data['is_agg'] = 0
        de_duped_agg_df['is_agg'] = 1

        ##  union the two data frames but differentiate aggregation
        unioned_df = concat([df_w_data,de_duped_agg_df])

        if len(unioned_df) == 0:
            err = 'There is no data (both aggregated and disaggregated) for the regions, campaigns, and indicators requested'
            return err, None

        sorted_df = self.sort_rc_df(unioned_df,campaigns)

        ## slice the unioned DF with the offset / limit provided
        offset_df = sorted_df[the_offset:the_limit + the_offset]

        if len(unioned_df) <= the_offset:
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

        ## try to find optional parameters in the dictionary. If they are not
        ## there return the default values ( given in the dict below)
        optional_params = {'the_limit':10000,'the_offset':0,'agg_level':'mixed',\
            'campaign_start':'2012-01-01','campaign_end':'2900-01-01' }


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


    def filter_campaigns_by_date(self,query_dict):
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

        return None, campaign__in


    def dp_df_to_list_of_results(self,dp_df,r_c_df,indicators):
        '''
        One problem with the way this code is writen is that when querying for
        region / campaign tuples, i chose to query where region__in [rs] and
        indicator__in [is].  THis means that the query you get back may result
        in more region / campaign couples that you initially expected.

        The alternative is to query one time per r / c couple but that isnt
        efficient.  So instead my code categorically ignores this when getting
        the data for regions and campaigns provided, and instead i use this method
        to filter (based on the r_c_df) the results in the dp_df with the keys that
        i must return to the api ( which exists in r_c_df )
        '''

        results = []

        results_dict = defaultdict(list)

        pivoted_dp_dict = self.pivot_dp_df(dp_df,'value')
        pivoted_id_dict = self.pivot_dp_df(dp_df,'id')
        pivoted_is_agg_dict = self.pivot_dp_df(dp_df,'is_agg')

        for row_ix, row_data in r_c_df.iterrows():

            # instantiate a result object ( one result per response )
            new_obj = ResultObject()

            # find the region and campaign from the row in the r_c dataframe
            region_id = int(row_data.region_id)
            campaign_id = int(row_data.campaign_id)

            ## add region / campaign from the r_c_df created initially
            new_obj.region = region_id
            new_obj.campaign = campaign_id

            ## look up the indicators from the dictonary created above
            indicator_data = pivoted_dp_dict[(region_id,campaign_id)]

            ## if there is no data for a requested indicator i need
            ## to explicitly add none for that ID
            for ind in indicators:
                try:
                    indicator_data[ind]
                except KeyError:
                    indicator_data[ind] = None

            # prepare a list of dicts to add to the r/c key
            indicator_list = []

            ## iterate through the indicators, create a dictionary with relevant
            ## data and append it to the result object.
            for k,v in indicator_data.iteritems():
                ind_dict = {}

                ## try to find the is_agg and datapoint id for the indicator / value
                ## If there was no data, set the is_agg, dp_id and val = None
                try:
                    datapoint_id = pivoted_id_dict[(region_id,campaign_id)][k]
                    is_agg = pivoted_is_agg_dict[(region_id,campaign_id)][k]
                except KeyError:
                    datapoint_id,is_agg,v = float('NaN'),float('NaN'),float('NaN')

                ind_dict['datapoint_id'] = None if isnan(float(datapoint_id)) else datapoint_id
                ind_dict['indicator'] = k
                ind_dict['value'] = None if isnan(float(v)) else v
                ind_dict['is_agg'] =  None if isnan(float(is_agg)) else is_agg

                indicator_list.append(ind_dict)

            new_obj.indicators = indicator_list

            results.append(new_obj)

        return results


    def build_stored_df(self,campaigns,indicators,regions):

        ## find data for the requested regions campaigns and indicators
        ## get datapoints according to regions/campaigns/indicators ##
        dp_columns = ['id','indicator_id','campaign_id','region_id','value']

        try:
            dp_df = DataFrame(list(AbstractedDataPoint.objects.filter(
                region__in = regions,\
                campaign__in = campaigns,\
                indicator__in = indicators).values()))[dp_columns]
        except KeyError:
            dp_df = DataFrame(columns=dp_columns)

        return dp_df


    def build_aggregate_df(self,campaigns,indicators,regions):
        '''
        Taking the keys that are missing data.. find the child regions
        and query the AbstractedDataPoints table, returning the aggregate value for
        each parent region, indicator, campaign combo.

        I would really like to be explicit about the c,i,r thing tuple set.
        I'm usign the convention for alphabetical order, but i want to make this
        explicit with either a dictionary or dataframe.
        '''

        ## we should get back one row for each of the tuples below
        expected_data = set(product(campaigns,indicators,regions))

        ## this is the data that exists for the keys given
        key_combos_with_data = set(AbstractedDataPoint.objects.filter(
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

            sum_of_child_regions = AbstractedDataPoint.objects.filter(
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


    def build_agg_rc_df(self,campaigns,indicators,regions):
        '''
        This method lets me find the region / campaign couples for which there
        is aggregated data.
        '''

        parent_region_lookup = []
        all_children = []

        ## create a lookup where the key is the child
        ## region and the parent is the value
        for r in regions:

            try:
                r_obj = Region.objects.get(id=r)
            except ObjectDoesNotExist as err:
                return str(err) + ' for region_id: ' + str(r) , None

            for chld in r_obj.get_all_children():
                parent_region_lookup.append([chld.id,r])
                all_children.append(chld.id) ## this is kinda lame

        ## build a dataframe where we trying to find all of the distinct
        ## campaign/indicator/child_region combbos.  # if none, return empty df
        try:
            children_regions_with_data_df = DataFrame(list(AbstractedDataPoint.objects.filter(
                campaign__in = campaigns,\
                indicator__in = indicators,\
                region__in = set(all_children)).values_list(\
                'campaign','region').distinct()),columns= \
                    ['campaign_id','child_region_id'])

        except ValueError:
            children_regions_with_data_df = DataFrame(columns= \
                ['campaign_id','child_region_id'])

        ## create a data frame from the parent_region lookup created above ##
        try:
            region_lookup_df = DataFrame(parent_region_lookup,columns=\
                ['child_region_id','region_id'])
        except ValueError:
            region_lookup_df = DataFrame(columns=['child_region_id','region_id'])

        ## inner join the two dataframes above wtih the objective of finding
        ## the distinct campaing, indicators and PARENT_region
        parent_lookup_df = merge(children_regions_with_data_df,region_lookup_df,\
            on='child_region_id')

        ## dedupe the dataframe findinf the regions/campaings/indicators
        ## that have data at the level of the child.
        de_duped_agg_df = parent_lookup_df.drop_duplicates(subset = \
         ['campaign_id','region_id'])

        r_c_df = de_duped_agg_df.drop('child_region_id', 1)

        return None, r_c_df


    def sort_rc_df(self,rc_df,campaigns):
        '''
        This sorts the result object and determines what will be sliced by
        the offset and the limit.  For now i'm defaulting the sorting to be on
        campaign date descending, but am setting this up to allow for more
        complex filtering later on.
        '''

        ## find the start dates of the campaigns ##
        campaign_id_start_date_df = DataFrame(list(Campaign.objects.filter(id__in = \
            campaigns).values_list('id','start_date').distinct()),\
            columns=['campaign_id','start_date'])

        ## join the two dataframes, finding the start_date ##
        r_c_w_start_date_df = rc_df.merge(campaign_id_start_date_df,on='campaign_id')
        sorted_rc_df = r_c_w_start_date_df.sort(columns = 'start_date',\
            ascending = False )

        return sorted_rc_df



    def pivot_dp_df(self,dp_df,value_column):
        '''
        this method takes a dataframe with datapoints table like data and transforms
        it into an object where the region / campaign is the key and the values
        are dictionares with the keys specified via the value column.
        '''

        pivoted_dict = pivot_table(dp_df, values = value_column, index=['region_id',\
            'campaign_id'], columns = ['indicator_id'], aggfunc = lambda x: x)\
            .transpose().to_dict()

        return pivoted_dict


    def check_db_for_indicators(self,tmp_indicators):

        indicator_ids = Indicator.objects.filter(id__in=tmp_indicators).values_list('id',flat=True)

        not_in_db = set(tmp_indicators).difference(set(indicator_ids))

        if len(not_in_db) > 0:
            err = 'indicator_id: ' + str(list(not_in_db)[0]) + ' does not exists.'
            return err, None

        return None, list(indicator_ids)


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
