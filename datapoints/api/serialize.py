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

        pp.pprint(meta_lookup)

        expanded_objects = []

        for obj in data_objects:
            expanded_obj = {}
            print '---'
            print obj
            expanded_obj['region'] = meta_lookup['region'][obj['region']]
            expanded_obj['campaign'] = meta_lookup['campaign'][obj['campaign']]

            for ind_dict in obj['indicators']:
                ind = meta_lookup['indicator'][ind_dict['indicator']]
                val = ind_dict['value']
                expanded_obj[ind] = val

            expanded_objects.append(expanded_obj)


        some_df = DataFrame(expanded_objects)#[['region','campaign']]
        print some_df

        csv = StringIO.StringIO(str(some_df.to_csv(index=False)))
        return csv

    def build_meta_lookup(self,object_list):

        meta_lookup = {}

        region_ids = [obj['region'] for obj in object_list]
        campaign_ids = [obj['campaign'] for obj in object_list]

        indicator_dicts = [obj['indicators'] for obj in object_list]

        indicator_ids = []

        for ind in indicator_dicts:
            for other_ind in ind:
                indicator_ids.append(other_ind['indicator'])


        regions = Region.objects.filter(id__in=region_ids)#.values_list('id','name')
        campaigns = Campaign.objects.filter(id__in=campaign_ids)
        indicators = Indicator.objects.filter(id__in=indicator_ids)


        region_lookup = {}
        for r in regions:
            region_lookup[r.id] = r.__unicode__()


        campaign_lookup = {}
        for c in campaigns:
            campaign_lookup[c.id] = c.__unicode__()


        indicator_lookup = {}
        for ind in indicators:
            indicator_lookup[ind.id] = ind.__unicode__()


        meta_lookup['region'] = region_lookup
        meta_lookup['campaign'] = campaign_lookup
        meta_lookup['indicator'] = indicator_lookup


        pp.pprint(meta_lookup)
        return meta_lookup
