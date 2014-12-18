import StringIO

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

        list_of_rows = []

        ## prep metadata (indicator/region/campaign names) for lookup later
        indicator_dicts = [row['indicators'] for row in data_objects]
        indicator_ids= [int(i_dct[0]['indicator']) for i_dct in indicator_dicts]
        indicator_lookup = self.build_meta_lookup(Indicator,indicator_ids)

        region_ids = [int(row['region']) for row in data_objects]
        region_lookup = self.build_meta_lookup(Region,region_ids)

        campaign_ids = [int(row['campaign']) for row in data_objects]
        campaign_lookup = self.build_meta_lookup(Campaign,campaign_ids)

        for row in data_objects:#.iteritems():
            row_dict = {}
            row_dict['region'] = region_lookup[row['region']]
            row_dict['campaign'] = campaign_lookup[row['campaign']]

            indicators = row['indicators']
            for ind in indicators:

                row_dict[indicator_lookup[int(ind['indicator'])]] = ind['value']

            list_of_rows.append(row_dict)

        csv_df = DataFrame(list_of_rows,index=None)
        csv = StringIO.StringIO(str(csv_df.to_csv(index=False)))

        return csv

    def build_meta_lookup(self,object_type,meta_ids):

        meta_lookup = {}

        for the_id in set(meta_ids):

            meta_lookup[the_id] = object_type.objects.get(id=the_id).name

        return meta_lookup
