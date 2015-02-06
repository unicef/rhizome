import StringIO
import pprint as pp

from tastypie.serializers import Serializer
from pandas import DataFrame

from datapoints.models import Campaign, Indicator, Region

class CustomSerializer(Serializer):
    formats = ['json', 'csv']
    content_types = {
        'json': 'application/json',
        'csv': 'text/csv',
    }


    def to_csv(self, data, options=None):
        '''
        First lookup the metadata (campaign, region, indicator) and build a map
        cooresponding to id / name.  Afterwords iterate through the dataobjecst
        passed, unpack the indicator objects and create a dataframe which gets
        converted to a csv.
        '''

        options = options or {}
        data = self.to_simple(data, options)
        data_objects = data['objects']

        meta_lookup = self.build_meta_lookup(data_objects)

        expanded_objects = []

        for obj in data_objects:

            expanded_obj = {}

            expanded_obj['region'] = meta_lookup['region'][obj['region']]
            expanded_obj['campaign'] = meta_lookup['campaign'][obj['campaign']]

            for ind_dict in obj['indicators']:
                try:
                    ind = meta_lookup['indicator'][ind_dict['indicator']]
                except KeyError:
                    ind = ''
                    pass

                val = ind_dict['value']
                expanded_obj[ind] = val

            expanded_objects.append(expanded_obj)

        csv_df = DataFrame(expanded_objects)#[['region','campaign']]

        ## rearrange column order ( POLIO-200 ) ##
        ## http://stackoverflow.com/questions/13148429 ##
        cols = csv_df.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        csv_df = csv_df[cols]


        csv = StringIO.StringIO(str(csv_df.to_csv(index=False)))
        return csv

    def build_meta_lookup(self,object_list):
        '''
        Instead of hitting the datbase every time you need to find the
        string for a particular meta data item.. build a dictionary
        once, store it in memory and access metadata values this way.

        '''
        # set up the lookup object
        meta_lookup = {'region':{},'campaign':{},'indicator':{}}

        ## find the region and campaign ids from the object list
        region_ids = [obj['region'] for obj in object_list]
        campaign_ids = [obj['campaign'] for obj in object_list]

        ## every object has all indicators, so find the first one, and the IDs
        ## for each indicator in that object
        indicator_list = [obj['indicators'] for obj in object_list]
        indicator_ids = [ind_dict['indicator'] for ind_dict in indicator_list[0]]


        for r in Region.objects.filter(id__in=region_ids):
            meta_lookup['region'][r.id] = r.__unicode__()

        for c in Campaign.objects.filter(id__in=campaign_ids):
            meta_lookup['campaign'][c.id] = c.__unicode__()

        for ind in Indicator.objects.filter(id__in=indicator_ids):
            meta_lookup['indicator'][ind.id] = ind.__unicode__()


        return meta_lookup
