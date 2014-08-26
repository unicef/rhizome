import sys, os
sys.path.append('/Users/johndingee_seed/code/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polio.settings'
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datapoints.models import Indicator, DataPoint, Region, Campaign
from source_data.models import VCMSummaryNew

from dateutil import parser

import pprint as pp
import pandas as pd

class VcmEtl(object):
    def __init__(self):

        self.inds = Indicator.objects.all()
        self.to_process = pd.DataFrame(list(VCMSummaryNew.objects.all().values())) # where processed = 0
        self.source_columns = VCMSummaryNew._meta.get_all_field_names()

        # map columns to indicators #
        self.column_to_indicator_map = {}
        for col in self.source_columns:
            if col in [ind.name for ind in self.inds]:
                self.column_to_indicator_map[col] = Indicator.objects.get(name=col).id


    def process_data(self):

        # map rows to region / campaigns {<row_id>:(<region_id>,<campaign_id>)}  #
        row_to_region_campaign_map = {}

        meta_columns = ['id','Date_Implement','SettlementCode',]
        indicator_columns = [col for col,ind_id in self.column_to_indicator_map.iteritems()]
        slice_columns = meta_columns + indicator_columns

        sliced_df = self.to_process[slice_columns]
        column_list = sliced_df.columns.tolist()

        for row in sliced_df.values:
            self.proces_row(row,column_list,self.column_to_indicator_map)


    def proces_row(self,row,column_names,column_to_indicator_map):

        try:
            region_id = Region.objects.get(full_name=row[column_names.index \
                ('SettlementCode')]).id ## evaluate this by settlement code not name

        except ObjectDoesNotExist:
            return None

        try:
            the_date = parser.parse(row[column_names.index('Date_Implement')])
            campaign_id = Campaign.objects.get(start_date=the_date).id
            print campaign_id
        except ObjectDoesNotExist:
            return None

        for i, value in enumerate(row):

            try:
                indicator_id =  self.column_to_indicator_map[column_names[i]]
            except KeyError:
                return # means it is a meta data column

            cell_value = row[i]
            dp = self.process_cell(region_id,campaign_id,indicator_id,cell_value)



    def process_cell(self,region_id,campaign_id,indicator_id,cell_value):

        if cell_value == "":
            return

        try:
            dp = DataPoint.objects.create(
                indicator_id = indicator_id, \
                region_id = region_id, \
                campaign_id = campaign_id, \
                value =  datapoint_value, \
                changed_by_id = 1  # FIX THIS! User should be "ODK ETL"
            )
        except IntegrityError:
            return # means this is a duplicative datapoint.
            # we are going to have to deal with the situation in which
            # the VWS re-enters the data.  This will have to be a merge
            # i.e. try to enter, if integrity error, then update.


if __name__ == "__main__":
    # vcm_summary()
    v = VcmEtl()
    v.process_data()
