import sys, os
sys.path.append('/Users/johndingee_seed/code/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polio.settings'
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datapoints.models import Indicator, DataPoint, Region, Campaign, Office
from source_data.models import VCMSummaryNew

from dateutil import parser

import pprint as pp
import pandas as pd


class MetaDataEtl(object):
    def __init__(self):
        print 'Begin Meta Data Ingest'

        # self.ingest_indicators()
        self.ingest_campaigns()

    def ingest_indicators(self):

        non_indicator_fields = ['SubmissionDate','deviceid','simserial',\
            'phonenumber','DateOfReport','Date_Implement','SettlementCode',\
            'meta_instanceID','KEY']

        v = VCMSummaryNew()
        all_fields = v._meta.fields

        indicators = []
        for f in all_fields:
            if f.name not in non_indicator_fields:
                indicators.append(f.name)

        for i in indicators:
            try:
                created = Indicator.objects.create(name = i,description = i, \
                  is_reported = 1)
            except IntegrityError:
                pass

    def ingest_regions(self):
        pass

    def ingest_campaigns(self):
        all_data = VCMSummaryNew.objects.all()
        all_campaigns = []

        # Ensure the Office ID is in there
        try:
            ng_office_id = Office.objects.get(name='Nigeria')
        except ObjectDoesNotExist:
            ng_office = Office.objects.create(name='Nigeria')
            ng_office_id = ng_office.id

        for row in all_data:
            print row.Date_Implement

            created = Campaign.objects.create(
                name = 'Nigeria Starting:' + row.Date_Implement, \
                office = ng_office_id, \
                start_date = parser.parse(row.Date_Implement), \
                end_date = parser.parse(row.Date_Implement)
            )


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
            self.proces_row(row,column_list)


    def proces_row(self,row,column_names):

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
                cell_value = row[i]
                dp = self.process_cell(region_id,campaign_id,indicator_id,cell_value)
                ## Clean this up ^^ ##
            except KeyError as e:
                pass # means it is a meta data column



    def process_cell(self,region_id,campaign_id,indicator_id,cell_value):

        if cell_value == "":
            return

        try:
            dp = DataPoint.objects.create(
                indicator_id = indicator_id, \
                region_id = region_id, \
                campaign_id = campaign_id, \
                value =  cell_value, \
                changed_by_id = 1  # FIX THIS! User should be "ODK ETL"
            )
        except IntegrityError:
            return # means this is a duplicative datapoint.
            # we are going to have to deal with the situation in which
            # the VWS re-enters the data.  This will have to be a merge
            # i.e. try to enter, if integrity error, then update.


if __name__ == "__main__":
    m = MetaDataEtl()
    m.ingest_indicators()
    # v = VcmEtl()
    # v.process_data()
