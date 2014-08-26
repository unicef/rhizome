import sys, os
sys.path.append('/Users/johndingee_seed/code/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polio.settings'
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist
from datapoints.models import Indicator, DataPoint, Region, Campaign
from odk_source.models import VCMSummaryNew

from dateutil import parser



import pprint as pp
import pandas as pd

def vcm_summary():

    inds = Indicator.objects.all()

    to_process = pd.DataFrame(list(VCMSummaryNew.objects.all().values())) # where processed = 0
    source_columns = VCMSummaryNew._meta.get_all_field_names()

    # map columns to indicators #
    column_to_indicator_map = {}
    for col in source_columns:
        if col in [ind.name for ind in inds]:
            column_to_indicator_map[col] = Indicator.objects.get(name=col).id

    # map rows to region / campaigns {<row_id>:(<region_id>,<campaign_id>)}  #
    row_to_region_campaign_map = {}

    meta_columns = ['id','Date_Implement','SettlementCode',]
    indicator_columns = [col for col,ind_id in column_to_indicator_map.iteritems()]
    slice_columns = meta_columns + indicator_columns

    sliced_df = to_process[slice_columns]

    for row in sliced_df.values:
        new_dp = proces_row(row,sliced_df.columns.tolist())


def proces_row(row,column_names):

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







if __name__ == "__main__":
    vcm_summary()
