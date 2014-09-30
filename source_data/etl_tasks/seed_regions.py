import sys,os
import pandas as pd

sys.path.append('/Users/johndingee_seed/code/UF04/polio')
sys.path.append('/Users/johndingee_seed/code/UF04/polio/polio')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from source_data.models import VCMSettlement, SourceRegion


def main():

    setts = VCMSettlement.objects.all()

    region_strings = []

    to_process_df = pd.DataFrame(list(VCMSettlement.objects.values()))

    for row in to_process_df.values:
        row_dict = {}

        row_dict['full_name'] = row[cols.index('settlementname')]
        row_dict['settlement_code'] = row[cols.index('settlementcode')]
        row_dict['latitude'] = row[cols.index('settlementgps_latitude')]
        row_dict['longitude'] = row[cols.index('settlementgps_longitude')]
        row_dict['longitude'] = row[cols.index('settlementgps_longitude')]
        row_dict['source_guid'] = row[cols.index('key')]


if __name__ == "__main__":
    main()
