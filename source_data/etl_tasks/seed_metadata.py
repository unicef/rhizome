import sys,os
import pandas as pd
import traceback

sys.path.append('/Users/johndingee_seed/code/UF04/polio')
sys.path.append('/Users/johndingee_seed/code/UF04/polio/polio')

os.environ['DJANGO_SETTINGS_MODULE'] = 'prod_settings'

from source_data.models import VCMSettlement, SourceRegion
from datapoints.models import Indicator,Region,Source,Office
from django.db import IntegrityError

def seed_regions():

    to_process_df = pd.DataFrame(list(VCMSettlement.objects.values()))
    cols = [col.lower() for col in to_process_df]

    for row in to_process_df.values:
        row_dict = {}

        row_dict['full_name'] = row[cols.index('settlementname')]
        row_dict['settlement_code'] = row[cols.index('settlementcode')]
        row_dict['latitude'] = row[cols.index('settlementgps_latitude')]
        row_dict['longitude'] = row[cols.index('settlementgps_longitude')]
        row_dict['longitude'] = row[cols.index('settlementgps_longitude')]
        row_dict['source_guid'] = row[cols.index('key')]
        row_dict['source_id'] = Source.objects.get(source_name='data entry').id
        row_dict['office_id'] = Office.objects.get(name='Nigeria').id

        try:
            Region.objects.create(**row_dict)
        except IntegrityError:
            err = traceback.format_exc()
            print err

def seed_indicators():

    df = pd.read_csv('/Users/johndingee_seed/Desktop/johns_inds.csv')



    for row in df.values:
        to_create = {}

        to_create['name'] =  row[0]
        to_create['description'] =  row[1]
        to_create['is_reported'] =  1

        try:
            Indicator.objects.create(**to_create)

        except Exception as e:
            print e


if __name__ == "__main__":
    seed_indicators()
    seed_regions()
