import sys, os
sys.path.append('/Users/johndingee_seed/code/polio')
os.environ['DJANGO_SETTINGS_MODULE'] = 'polio.settings'

from django.conf import settings
from datapoints.models import Indicator, DataPoint,Region
from odk_source.models import VCMSummaryNew

import pprint as pp

def vcm_summary():
    inds = Indicator.objects.all()

    to_process = VCMSummaryNew.objects.all() # where processed = 0
    source_columns = VCMSummaryNew._meta.get_all_field_names()

    column_to_indicator_map = {}

    for col in source_columns:
        if col in [ind.name for ind in inds]:
            print col
            column_to_indicator_map[col] = Indicator.objects.get(name=col).id

            # region_id = Region.objects.find(full_name = )

    pp.pprint(column_to_indicator_map)





if __name__ == "__main__":
    vcm_summary()
